# Coffee research and Ahmedabad café model

| File | What it is |
|---|---|
| `Coffee_Deep_Dive_and_Cafe_Model.pdf` | 91-page report. Part 1: coffee from seed to cup and its market. Part 2: inputs and outputs of the café model |
| `Cafe_Financial_Model.xlsx` | Interactive 3-statement + FCFF DCF model (location, premises, roasting route, bean mix, scenario switches; live data tables) |
| `Final_Coff.pdf` | Earlier 19-page field guide to judging coffee quality |

## Regenerating

```
python3 cafe_model/build_excel.py       # workbook (recalculated headlessly in LibreOffice)
python3 cafe_model/export_results.py    # runs every configuration/scenario -> cafe_model/results.json
python3 build_deep_report.py            # the PDF (Part 2 numbers come from results.json)
python3 build_report.py                 # the earlier field guide
```

All model assumptions live in `cafe_model/assumptions.py` and appear as blue input cells in the workbook.
Requires ReportLab, xlsxwriter, numpy, Pillow, pypdf and LibreOffice (for recalculation).
