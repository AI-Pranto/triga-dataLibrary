import requests
import zipfile
import io
import os

isotopes = [("H1",    "n_0125_1-H-1.zip"), 
            ("H2",    "n_0128_1-H-2.zip"), 
            ("O16",   "n_0825_8-O-16.zip"),
            ("U235",  "n_9228_92-U-235.zip"),
            ("U238",  "n_9237_92-U-238.zip"),
            ("Zr90",  "n_4025_40-Zr-90.zip"),
            ("Er166", "n_6837_68-Er-166.zip"),
            ("Er167", "n_6840_68-Er-167.zip"),
            ("Mo98",  "n_4243_42-Mo-98.zip"),
            ("C0",    "n_0600_6-C-0.zip"),
            ("Cr50",  "n_2425_24-Cr-50.zip"),
            ("Cr52",  "n_2431_24-Cr-52.zip"),
            ("Cr53",  "n_2434_24-Cr-53.zip"),
            ("Cr54",  "n_2437_24-Cr-54.zip"),
            ("Fe54",  "n_2625_26-Fe-54.zip"),
            ("Fe56",  "n_2631_26-Fe-56.zip"),
            ("Fe57",  "n_2634_26-Fe-57.zip"),
            ("Fe58",  "n_2637_26-Fe-58.zip"),
            ("Ni58",  "n_2825_28-Ni-58.zip"),
            ("Ni60",  "n_2831_28-Ni-60.zip"),
            ("Ni61",  "n_2834_28-Ni-61.zip"),
            ("Ni62",  "n_2837_28-Ni-62.zip"),
            ("Ni64",  "n_2843_28-Ni-64.zip"),
            ("Mn55",  "n_2525_25-Mn-55.zip"),
            ("Si28",  "n_1425_14-Si-28.zip"),
            ("Si29",  "n_1428_14-Si-29.zip"),
            ("Si30",  "n_1431_14-Si-30.zip"),
            ("N14",   "n_0725_7-N-14.zip"),
            ("N15",   "n_0728_7-N-15.zip"),
            ("P31",   "n_1525_15-P-31.zip"),
            ("S32",   "n_1625_16-S-32.zip"),
            ("S33",   "n_1628_16-S-33.zip"),
            ("S34",   "n_1631_16-S-34.zip"),
            ("S36",   "n_1637_16-S-36.zip"),
            ("B10",   "n_0525_5-B-10.zip"),
            ("B11",   "n_0528_5-B-11.zip"),
            ("Zr91",  "n_4028_40-Zr-91.zip"),
            ("Zr92",  "n_4031_40-Zr-92.zip"),
            ("Zr94",  "n_4037_40-Zr-94.zip"),
            ("Zr96",  "n_4043_40-Zr-96.zip"),
            ("Mg24",   "n_1225_12-Mg-24.zip"),
            ("Al27",   "n_1325_13-Al-27.zip"),
            ("Cu63",   "n_2925_29-Cu-63.zip"),
            ("Cu65",   "n_2931_29-Cu-65.zip"),
            ("Zn64",   "n_3025_30-Zn-64.zip"),
            ("Pb207",  "n_8234_82-Pb-207.zip"),
            ("HinH2O", "tsl_0001_h(h2o).zip"),
            ("ZrinZrH","tsl_0058_zr(zrh).zip"),
            ("HinZrH", "tsl_0007_h(zrh).zip")]

for iso in isotopes:
    iso_name, file_name = iso[0], iso[1]
    if file_name:
        if iso_name in ['C0', 'Si28', 'Si29']:
            url = f"https://www-nds.iaea.org/public/download-endf/JEFF-3.3/n/{file_name}"
        else:
            url = f"https://www-nds.iaea.org/public/download-endf/JENDL-4.0u2-20160106/{'n' if 'n_' in file_name else 'tsl'}/{file_name}"
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        os.rename(f"{file_name.split('.')[0]}.dat", f"{iso_name}.dat")

