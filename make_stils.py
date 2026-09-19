from PIL import Image
for name in ["lemma21_case_b", "lemma21_case_c", "lemma21_case_vertical"]:
    im = Image.open(f"figs/chapter2/lemma21/{name}.gif")
    im.seek(im.n_frames - 1)              # final frame: o has reached a or b
    im.convert("RGB").save(f"figs/chapter2/lemma21/{name}.png")
