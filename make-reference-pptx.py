"""Build ki-reference.pptx (pandoc/Quarto reference doc) from assets/ki-template.potx.

Pandoc only accepts a .pptx reference doc and finds layouts by their English
names. This script copies the KI template, marks it as a presentation instead
of a template, and renames the KI layouts that pandoc uses:

  Startbild                 -> Title Slide
  Avsnittsbild              -> Section Header
  Rubrik och innehåll       -> Title and Content
  Rubrik + 2 innehållsdelar -> Two Content

Only needed when the KI template changes. Run from anywhere:
  python3 quarto-theme-ki/make-reference-pptx.py
"""
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "ki-template.potx")
DST = os.path.join(HERE, "ki-reference.pptx")

RENAME = {
    "Startbild": "Title Slide",
    "Avsnittsbild": "Section Header",
    "Rubrik och innehåll": "Title and Content",
    "Rubrik + 2 innehållsdelar": "Two Content",
}

# Parts that pandoc does not copy into its output although it keeps the
# relationships pointing to them, which makes PowerPoint offer to repair the
# file. Drop them (and every reference to them) from the reference doc.
DROP = re.compile(r"customXml/|ppt/handoutMasters/")

with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if DROP.match(item.filename):
            continue
        data = zin.read(item.filename)
        if item.filename == "[Content_Types].xml":
            data = data.replace(
                b"presentationml.template.main+xml",
                b"presentationml.presentation.main+xml",
            )
            data = re.sub(rb'<Override PartName="/(customXml|ppt/handoutMasters)/[^>]*/>', b"", data)
        elif item.filename == "ppt/_rels/presentation.xml.rels":
            data = re.sub(rb'<Relationship [^>]*Target="(\.\./customXml|handoutMasters)/[^>]*/>', b"", data)
        elif item.filename == "ppt/presentation.xml":
            data = re.sub(rb"<p:handoutMasterIdLst>.*?</p:handoutMasterIdLst>", b"", data)
        elif re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", item.filename):
            text = data.decode("utf-8")
            for sv, en in RENAME.items():
                text = text.replace(f'<p:cSld name="{sv}"', f'<p:cSld name="{en}"')
            data = text.encode("utf-8")
        zout.writestr(item, data)

print(f"Wrote {DST}")
