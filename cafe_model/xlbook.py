"""Small layout engine on top of xlsxwriter for the café model.

Every row or cell that other formulas need is registered under a key.  The
workbook is laid out twice: pass 1 records where each key lands, pass 2 writes
the real formulas with every reference resolved.  A third pass can add cached
values computed by LibreOffice (see recalc.py).

Formula templates use these tokens:
  {key}       same timeline column of row `key`      {key@p}  previous column
  {key@L}     last timeline column (Y10)             {key@F}  first column (Y0)
  {key@3}     timeline column of year 3              {$key}   absolute scalar cell
  {#key}      whole timeline range F:P of row `key`  {#key:1} range Y1..Y10
"""
import re
import zipfile

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

NT = 11                      # Y0 .. Y10
TL0 = 5                      # timeline starts in column F
TC = [xl_col_to_name(TL0 + i) for i in range(NT)]
FONT = "Calibri"
BLUE, GREEN, BLACK, GREY = "#2A62C9", "#00803C", "#000000", "#7F7F7F"
BAND, BAND_TXT, SUB, INFILL = "#4E342E", "#FFFFFF", "#EFE6DD", "#FFF6DA"
HEAD_FILL = "#F6F1EB"

NUM = {
    "lakh": '_(#,##0.0_);\\(#,##0.0\\);_("–"_);_(@_)',
    "lakh2": '_(#,##0.00_);\\(#,##0.00\\);_("–"_);_(@_)',
    "int": '_(#,##0_);\\(#,##0\\);_("–"_);_(@_)',
    "pct": '_(#,##0.0%_);\\(#,##0.0%\\);_("–"_)_%;_(@_)_%',
    "pct2": '_(#,##0.00%_);\\(#,##0.00%\\);_("–"_)_%;_(@_)_%',
    "x": '_(0.00"x"_);\\(0.00"x"\\);_("–"_);_(@_)',
    "ix": '_(0.000_);\\(0.000\\);_("–"_);_(@_)',
    "fy": '"FY"0',
    "yr": '"Y"0',
    "yrs": '[>=99]">10 yrs";0.0" yrs"',
    "gen": "General",
    "idx": "0",
    "rs": '_(₹#,##0_);\\(₹#,##0\\);_("–"_);_(@_)',
}

TOK = re.compile(r"\{([$#]?)([A-Za-z_]\w*)(?:@(\w+))?(?::(\d+))?(?::(\d+))?\}")


class Book:
    def __init__(self, path, reg=None, cache=None):
        self.path = path
        self.wb = xlsxwriter.Workbook(path)
        self.final = reg is not None
        self.reg = dict(reg) if reg else {}
        self.cache = cache or {}
        self.fmts, self.ws, self.r, self.kind, self.order = {}, {}, {}, {}, []
        self.cur = None
        self.calc_cells = []          # (sheet, row, col) of formulas & table results
        self.tables = []              # data tables to inject after closing
        self.names = {}

    # ------------------------------------------------------------------ sheets
    def add_sheet(self, name, tab, kind="timeline"):
        ws = self.wb.add_worksheet(name)
        ws.set_tab_color(tab)
        ws.hide_gridlines(2)
        ws.set_zoom(90)
        ws.set_default_row(15)
        self.ws[name], self.r[name], self.kind[name] = ws, 0, kind
        self.order.append(name)
        if kind == "timeline":
            ws.set_column(0, 0, 2)
            ws.set_column(1, 1, 46)
            ws.set_column(2, 2, 12)
            ws.set_column(3, 3, 13)
            ws.set_column(4, 4, 2)
            ws.set_column(TL0, TL0 + NT - 1, 11)
            ws.set_column(TL0 + NT, TL0 + NT, 2)
            ws.set_column(TL0 + NT + 1, TL0 + NT + 1, 60)
        ws.set_landscape()
        ws.set_paper(9)
        ws.fit_to_pages(1, 0)
        return ws

    def use(self, name):
        self.cur = name
        return self.ws[name]

    # ------------------------------------------------------------------ registry
    def _set(self, key, r, c):
        k = (self.cur, r, c)
        if self.final:
            if self.reg.get(key) != k:
                raise ValueError(f"layout drift for {key}: {self.reg.get(key)} vs {k}")
        else:
            if key in self.reg:
                raise ValueError("duplicate key " + key)
            self.reg[key] = k

    def _get(self, key):
        if key in self.reg:
            return self.reg[key]
        if self.final:
            raise KeyError(key)
        return (self.cur, 0, 0)

    def _pre(self, sheet):
        return "" if sheet == self.cur else f"{sheet}!"

    def s(self, key):
        sh, r, c = self._get(key)
        return f"{self._pre(sh)}${xl_col_to_name(c)}${r + 1}"

    def t(self, key, col):
        sh, r, _ = self._get(key)
        return f"{self._pre(sh)}{col}{r + 1}"

    def rg(self, key, i0=0, i1=NT - 1):
        sh, r, _ = self._get(key)
        return f"{self._pre(sh)}${TC[i0]}${r + 1}:${TC[i1]}${r + 1}"

    def area(self, k1, k2):
        sh, r1, c1 = self._get(k1)
        _, r2, c2 = self._get(k2)
        return (f"{self._pre(sh)}${xl_col_to_name(c1)}${r1 + 1}:"
                f"${xl_col_to_name(c2)}${r2 + 1}")

    def abs_addr(self, key):
        sh, r, c = self._get(key)
        return f"{sh}!${xl_col_to_name(c)}${r + 1}"

    def fx(self, tmpl, c=None, p=None):
        def rep(m):
            kind, key, at, a, b = m.groups()
            if kind == "$":
                return self.s(key)
            if kind == "#":
                return self.rg(key, int(a) if a else 0, int(b) if b else NT - 1)
            if at is None:
                col = c
            elif at == "p":
                col = p
            elif at == "L":
                col = TC[-1]
            elif at == "F":
                col = TC[0]
            else:
                col = TC[int(at)]
            if col is None:
                raise ValueError("timeline token without column: " + m.group(0))
            return self.t(key, col)
        return TOK.sub(rep, tmpl)

    # ------------------------------------------------------------------ formats & cells
    def f(self, num=None, **kw):
        d = dict(font_name=FONT, font_size=10, valign="vcenter")
        if num:
            d["num_format"] = NUM.get(num, num)
        d.update({k: v for k, v in kw.items() if v is not None and v is not False})
        key = tuple(sorted(d.items()))
        if key not in self.fmts:
            self.fmts[key] = self.wb.add_format(d)
        return self.fmts[key]

    def put(self, r, c, v, num="lakh", inp=None, color=None, **kw):
        ws = self.ws[self.cur]
        if isinstance(v, str) and v.startswith("="):
            v = self.fx(v)
            col = color or (GREEN if "!" in v else BLACK)
            val = self.cache.get((self.cur, r, c), 0)
            if val is None:
                val = 0
            ws.write_formula(r, c, v, self.f(num, font_color=col, **kw), val)
            self.calc_cells.append((self.cur, r, c))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            if inp is False:
                ws.write_number(r, c, v, self.f(num, font_color=color or BLACK, **kw))
            else:
                kw.setdefault("bg_color", INFILL)
                ws.write_number(r, c, v, self.f(num, font_color=BLUE, **kw))
        elif v is None:
            ws.write_blank(r, c, None, self.f(num, **kw))
        else:
            if inp:
                kw.setdefault("bg_color", INFILL)
                ws.write_string(r, c, v, self.f(None, font_color=BLUE, **kw))
            else:
                ws.write_string(r, c, v, self.f(None, font_color=color or BLACK, **kw))

    def nr(self, n=1):
        r = self.r[self.cur]
        self.r[self.cur] += n
        return r

    def skip(self, n=1):
        self.r[self.cur] += n

    def width(self):
        return TL0 + NT if self.kind[self.cur] == "timeline" else 12

    # ------------------------------------------------------------------ building blocks
    def title(self, text, sub):
        ws = self.ws[self.cur]
        ws.set_row(0, 24)
        ws.write_string(0, 1, text, self.f(None, bold=True, font_size=16, font_color=BAND))
        ws.write_string(1, 1, sub, self.f(None, italic=True, font_color=GREY))
        self.put(2, 1, '="Model running: "&{$cfg_label}', num=None, bold=True, color="#9C4A1A")
        self.r[self.cur] = 4

    def timeline_header(self, fy_key, t_key, src=None):
        """FY and period header rows; `src` = FY row key to link to (None = define here)."""
        r = self.nr()
        self._set(fy_key, r, TL0)
        hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1)
        self.put(r, 1, "₹ lakh unless stated", num=None, italic=True, **hd)
        self.put(r, 2, "Units", num=None, **hd)
        self.put(r, 3, "Value", num=None, align="right", **hd)
        self.put(r, 4, None, **hd)
        for i, col in enumerate(TC):
            if src is None:
                v = "={$first_fy}" if i == 0 else f"={{{fy_key}@p}}+1"
            else:
                v = f"={{{src}}}"
            self.put(r, TL0 + i, self.fx(v, col, TC[i - 1] if i else None), num="fy",
                     align="right", **hd)
        r = self.nr()
        self._set(t_key, r, TL0)
        for i, col in enumerate(TC):
            self.put(r, TL0 + i, self.fx(f"={{{fy_key}}}-{{$first_fy}}", col), num="yr",
                     align="right", italic=True, color=GREY)
        self.put(r, 1, "Period (Y0 = pre-opening fit-out year)", num=None, italic=True, color=GREY)
        self.ws[self.cur].freeze_panes(r + 1, TL0)

    def band(self, text):
        r = self.nr()
        ws = self.ws[self.cur]
        ws.set_row(r, 18)
        for c in range(1, self.width()):
            ws.write_blank(r, c, None, self.f(None, bg_color=BAND))
        ws.write_string(r, 1, text, self.f(None, bold=True, font_size=11, font_color=BAND_TXT,
                                            bg_color=BAND))
        return r

    def head(self, text, note=None):
        r = self.nr()
        ws = self.ws[self.cur]
        for c in range(1, self.width()):
            ws.write_blank(r, c, None, self.f(None, bg_color=SUB))
        ws.write_string(r, 1, text, self.f(None, bold=True, bg_color=SUB))
        if note:
            ws.write_string(r, 2, note, self.f(None, italic=True, font_color=GREY, bg_color=SUB))
        return r

    def note(self, text, col=1):
        r = self.nr()
        self.put(r, col, text, num=None, italic=True, color=GREY)
        return r

    def line(self, key, label, unit, spec, num="lakh", start=0, end=NT - 1, bold=False,
             top=False, italic=False, note=None, indent=1):
        r = self.nr()
        if key:
            self._set(key, r, TL0)
        st = {}
        if bold:
            st["bold"] = True
        if italic:
            st["italic"] = True
        if top:
            st["top"] = 1
        self.put(r, 1, label, num=None, indent=0 if bold else indent, **st)
        self.put(r, 2, unit, num=None, color=GREY, italic=True, **({"top": 1} if top else {}))
        if top:
            self.put(r, 3, None, top=1)
            self.put(r, 4, None, top=1)
        for i, col in enumerate(TC):
            v = None
            if start <= i <= end:
                if callable(spec):
                    v = spec(i)
                elif isinstance(spec, dict):
                    v = spec.get(i, spec.get("*"))
                elif isinstance(spec, (list, tuple)):
                    v = spec[i]
                else:
                    v = spec
            if isinstance(v, str) and v.startswith("="):
                v = self.fx(v, col, TC[i - 1] if i else None)
            self.put(r, TL0 + i, v, num=num, **st)
        if note:
            self.put(r, TL0 + NT + 1, note, num=None, color=GREY, italic=True)
        return r

    def sc(self, key, label, unit, v, num="lakh", note=None, bold=False, col=3, dv=None,
           note_col=None, top=False):
        r = self.nr()
        if key:
            self._set(key, r, col)
        st = {"bold": True} if bold else {}
        if top:
            st["top"] = 1
        self.put(r, 1, label, num=None, indent=0 if bold else 1, **st)
        self.put(r, 2, unit, num=None, color=GREY, italic=True, **({"top": 1} if top else {}))
        if isinstance(v, str) and not v.startswith("="):
            self.put(r, col, v, num=None, inp=True, bold=True)
        else:
            self.put(r, col, v, num=num, **st)
        if dv:
            self.ws[self.cur].data_validation(r, col, r, col, dv)
        if note:
            nc = note_col if note_col is not None else (5 if col < 5 else col + 2)
            self.put(r, nc, note, num=None, color=GREY, italic=True)
        return r

    def define(self, name, ref):
        self.names[name] = ref

    # ------------------------------------------------------------------ data tables
    def data_table(self, name, down, down_in, outs=None, across=None, across_in=None,
                   out=None, num="lakh", down_labels=None, across_labels=None,
                   head_down="", width_out=None):
        """Excel what-if data table.  1-D: values `down` substituted into `down_in`,
        one column per output in `outs` [(header, key, num)].  2-D: also `across`
        values into `across_in` with single output `out`."""
        ws = self.ws[self.cur]
        two_d = across is not None
        hd = dict(bold=True, bg_color=HEAD_FILL, bottom=1, text_wrap=True, align="center")
        rh = self.nr()
        ws.set_row(rh, 30)
        self.put(rh, 1, head_down, num=None, **{**hd, "align": "left"})
        self.put(rh, 2, None, **hd)
        r0 = self.nr()
        if two_d:
            for j, lab in enumerate(across_labels or across):
                self.put(rh, 3 + j, str(lab), num=None, **hd)
            self.put(r0, 1, "Current model value →", num=None, italic=True, color=GREY)
            self.put(r0, 2, self.fx("={" + out + "}") if not out.startswith("=") else out,
                     num=num, color=GREY, italic=True)
            for j, v in enumerate(across):
                self.put(r0, 3 + j, v, num="gen", align="center", bold=True)
            ncols = len(across)
        else:
            for j, (h, key, _n) in enumerate(outs):
                self.put(rh, 3 + j, h, num=None, **hd)
                self.put(r0, 3 + j, "={" + key + "}", num=_n, color=GREY, italic=True)
            self.put(r0, 1, "Current model value →", num=None, italic=True, color=GREY)
            ncols = len(outs)
        first = self.r[self.cur]
        for i, v in enumerate(down):
            r = self.nr()
            lab = down_labels[i] if down_labels else str(v)
            if isinstance(lab, str) and lab.startswith("="):
                self.put(r, 1, lab, num=None)
            else:
                self.put(r, 1, lab, num=None)
            self.put(r, 2, v, num="gen", align="center", bold=True)
            for j in range(ncols):
                n = num if two_d else outs[j][2]
                val = self.cache.get((self.cur, r, 3 + j), 0)
                if isinstance(val, str):
                    self.put(r, 3 + j, val if val else "", num=None, inp=False, align="right")
                else:
                    self.put(r, 3 + j, float(val or 0), num=n, inp=False)
                self.calc_cells.append((self.cur, r, 3 + j))
        last = self.r[self.cur] - 1
        ref = f"{xl_col_to_name(3)}{first + 1}:{xl_col_to_name(3 + ncols - 1)}{last + 1}"
        spec = dict(sheet=self.cur, cell=f"{xl_col_to_name(3)}{first + 1}", ref=ref, first=first,
                    down=list(down), across=list(across) if two_d else None,
                    down_in=self._get(down_in), across_in=self._get(across_in) if two_d else None,
                    outs=[self.addr(out)] if two_d else [self.addr(k) for _h, k, _n in outs])
        if two_d:
            spec.update(dt2D=1, dtr=1, r1=self.s(across_in).replace("$", "").split("!")[-1],
                        r2=self.s(down_in).replace("$", "").split("!")[-1])
        else:
            spec.update(dt2D=0, dtr=0, r1=self.s(down_in).replace("$", "").split("!")[-1])
        self.tables.append(spec)
        self._set("dt_" + name, first, 3)
        return first, ncols

    def addr(self, token):
        """(sheet, row, col) of '$key', 'key@3', 'key@L' or 'key'."""
        token = token.lstrip("$")
        key, _, at = token.partition("@")
        sh, r, c = self._get(key)
        if at:
            c = TL0 + (NT - 1 if at == "L" else 0 if at == "F" else int(at))
        return (sh, r, c)

    def dref(self, name, i, j):
        sh, r, c = self._get("dt_" + name)
        return f"{self._pre(sh)}${xl_col_to_name(c + j)}${r + 1 + i}"

    # ------------------------------------------------------------------ finish
    def close(self, inject=True):
        for n, ref in self.names.items():
            self.wb.define_name(n, ref)
        self.wb.close()
        if inject:
            self._inject()

    def _inject(self):
        z = zipfile.ZipFile(self.path)
        files = {n: z.read(n) for n in z.namelist()}
        z.close()
        for spec in self.tables:
            idx = self.order.index(spec["sheet"]) + 1
            fn = f"xl/worksheets/sheet{idx}.xml"
            x = files[fn].decode("utf8")
            attrs = f'ref="{spec["ref"]}" dt2D="{spec["dt2D"]}" dtr="{spec["dtr"]}" r1="{spec["r1"]}"'
            if spec["dt2D"]:
                attrs += f' r2="{spec["r2"]}"'
            pat = re.compile(r'<c r="%s"([^>]*?)(/>|>(.*?)</c>)' % spec["cell"])
            m = pat.search(x)
            if not m:
                raise ValueError("data table anchor not found " + spec["cell"])
            inner = m.group(3) or ""
            vm = re.search(r"<v>.*?</v>", inner)
            v = vm.group(0) if vm else "<v>0</v>"
            a = re.sub(r'\s*t="\w+"', "", m.group(1))
            if "<is>" in inner or 't="s"' in m.group(1) or 't="str"' in m.group(1):
                v = "<v>0</v>"
            new = f'<c r="{spec["cell"]}"{a}><f t="dataTable" {attrs}/>{v}</c>'
            x = x[:m.start()] + new + x[m.end():]
            files[fn] = x.encode("utf8")
        wbx = files["xl/workbook.xml"].decode("utf8")
        wbx = re.sub(r"<calcPr([^/]*)/>",
                     lambda m: "<calcPr" + m.group(1).rstrip() +
                     ' iterate="1" iterateCount="100" iterateDelta="0.0001"/>', wbx)
        files["xl/workbook.xml"] = wbx.encode("utf8")
        with zipfile.ZipFile(self.path, "w", zipfile.ZIP_DEFLATED) as z:
            for n, d in files.items():
                z.writestr(n, d)
