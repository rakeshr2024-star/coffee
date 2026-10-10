"""Recalculate the workbook headlessly in LibreOffice (via UNO) and read values back.

Used to store cached values in the .xlsx (so viewers that do not recalculate still
show numbers) and to run the configuration/scenario loops that feed the PDF.
"""
import os
import subprocess
import time
from collections import defaultdict

import uno  # noqa: F401  (LibreOffice's Python bridge; system python3)
from com.sun.star.beans import PropertyValue


class Office:
    def __init__(self, port=2002):
        self.port = port
        self.proc = subprocess.Popen(
            ["soffice", "--headless", "--invisible", "--nologo", "--norestore", "--nodefault",
             f"--accept=socket,host=localhost,port={port};urp;"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local)
        ctx = None
        for _ in range(120):
            try:
                ctx = resolver.resolve(
                    f"uno:socket,host=localhost,port={port};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(0.5)
        if ctx is None:
            raise RuntimeError("LibreOffice did not start")
        self.desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        self.doc = None

    def open(self, path):
        pv = PropertyValue()
        pv.Name, pv.Value = "Hidden", True
        self.doc = self.desktop.loadComponentFromURL("file://" + os.path.abspath(path), "_blank", 0,
                                                     (pv,))
        self.doc.calculateAll()
        return self.doc

    def sheet(self, name):
        return self.doc.Sheets.getByName(name)

    def grid(self, name, nrows, ncols):
        rng = self.sheet(name).getCellRangeByPosition(0, 0, ncols - 1, nrows - 1)
        return rng.getDataArray()

    def set(self, name, row, col, value):
        self.sheet(name).getCellByPosition(col, row).setValue(value)

    def setstr(self, name, row, col, value):
        self.sheet(name).getCellByPosition(col, row).setString(value)

    def get(self, name, row, col):
        c = self.sheet(name).getCellByPosition(col, row)
        s = c.getString()
        t = c.getType().value
        if t == "TEXT":
            return s.strip()
        if t == "FORMULA":
            if c.getError():
                return "#ERR"
            if c.FormulaResultType2 == 2:      # com.sun.star.sheet.FormulaResult.STRING
                return s.strip()
        return c.getValue()

    def recalc(self):
        self.doc.calculateAll()

    def close(self):
        try:
            if self.doc is not None:
                self.doc.close(True)
        finally:
            self.proc.terminate()
            try:
                self.proc.wait(10)
            except Exception:
                self.proc.kill()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def col_idx(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def col_name(i):
    s = ""
    i += 1
    while i:
        i, rem = divmod(i - 1, 26)
        s = chr(65 + rem) + s
    return s


def emulate_tables(o, tables, out):
    """Fill `out` with what Excel's data tables will show, by setting each table's input
    cells and recalculating (LibreOffice's own TABLE() evaluation leaves stale values)."""
    for t in tables:
        ins = [t["down_in"]] + ([t["across_in"]] if t["across"] else [])
        saved = [o.get(*a) for a in ins]
        for i, dv in enumerate(t["down"]):
            o.set(*t["down_in"], dv)
            if t["across"]:
                for j, av in enumerate(t["across"]):
                    o.set(*t["across_in"], av)
                    o.recalc()
                    out[(t["sheet"], t["first"] + i, 3 + j)] = o.get(*t["outs"][0])
            else:
                o.recalc()
                for j, a in enumerate(t["outs"]):
                    out[(t["sheet"], t["first"] + i, 3 + j)] = o.get(*a)
        for a, v in zip(ins, saved):
            o.set(*a, v)
    o.recalc()


def values(path, cells, tables=()):
    """Return {(sheet, row, col): value} for formula cells and data-table results.
    `path` must be a copy of the workbook without injected data tables."""
    by = defaultdict(list)
    for s, r, c in cells:
        by[s].append((r, c))
    out = {}
    with Office() as o:
        o.open(path)
        for s, rc in by.items():
            nr = max(r for r, _ in rc) + 1
            nc = max(c for _, c in rc) + 1
            g = o.grid(s, nr, nc)
            for r, c in rc:
                v = g[r][c]
                out[(s, r, c)] = v.strip() if isinstance(v, str) else v
        emulate_tables(o, tables, out)
    return out
