from magic                          import Magic
import subprocess,os,re

mime = Magic(mime=True)

for drc in os.listdir("../sciencewashing/pdfs"):
    for fil in os.listdir(f"../sciencewashing/pdfs/{drc}"):
        if mime.from_file(fr"../sciencewashing/pdfs/{drc}/{fil}")=="application/pdf":
            #print(f"{drc}/{fil}")
            if not os.path.exists(f"../sciencewashing/grobid/{drc}"):
                os.makedirs(f"../sciencewashing/grobid/{drc}")
            if os.path.exists(f"../sciencewashing/grobid/{drc}/{fil[:-4]}.json"):
                pass
            else:
                subprocess.call([r"python", "external/s2orc-doc2json/doc2json/grobid2json/process_pdf.py", "-i", f"../sciencewashing/pdfs/{drc}/{fil}", "-o", f"../sciencewashing/grobid/{drc}/", "-t" "./temp_dir"])

