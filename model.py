from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, relationship
from datetime import date as dt_date
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
print("Password loaded as:", db_password)
engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/next_dr")

try:
    with engine.connect() as conn:
        print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__= "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    specialty: Mapped[str] = mapped_column()

class Term(Base):
    __tablename__="term"
    id: Mapped[int] = mapped_column(primary_key=True)
    term_name: Mapped[str] = mapped_column()
    clue1: Mapped[str] = mapped_column()
    clue2: Mapped[str] = mapped_column()
    clue3: Mapped[str] = mapped_column()
    clue4: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

class DailyTerm(Base):
    __tablename__ = "dailyterm"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[dt_date] = mapped_column()
    term_id: Mapped[int] = mapped_column(ForeignKey("term.id"))

Base.metadata.create_all(engine)

with Session(engine) as session:
    categoryDict = {"Cardiovascular": Category(specialty="Cardiovascular"), 
                    "Digestive": Category(specialty="Digestive"),
                    "Liver": Category(specialty="Liver"),
                    "Urinary": Category(specialty="Urinary"), 
                    "Nervous": Category(specialty="Nervous"),
                    "Skeletal": Category(specialty="Skeletal"),
                    "Integumentary": Category(specialty="Integumentary"),
                    "Respiratory": Category(specialty="Respiratory"),
                    "Circulatory": Category(specialty="Circulatory"),
                    }
    
    termsData = [
        # category_id 1 (Cardiovascular)
        {"term_name": "Cardiology", "clue1": "Cardiovascular", "clue2": "N/A -- this is a field of study, not a condition", "clue3": "study of", "clue4": "no extra chunk -- just \"heart\" + \"study of.\"", "category_id": 1},
        {"term_name": "Cardiomyopathy", "clue1": "Cardiovascular", "clue2": "Shortness of breath, fatigue, swelling in legs", "clue3": "disease/condition of", "clue4": "also contains a chunk meaning \"muscle\" -- a disease of the heart ______.", "category_id": 1},
        {"term_name": "Cardiac Arrest", "clue1": "Cardiovascular", "clue2": "Sudden collapse, no pulse, unresponsive", "clue3": "sudden stopping", "clue4": "no extra chunk -- just \"heart\" + \"stopping.\"", "category_id": 1},
        {"term_name": "Cardiogram", "clue1": "Cardiovascular", "clue2": "N/A -- a diagnostic tool/recording", "clue3": "a recording/tracing", "clue4": "no extra chunk -- just \"heart\" + \"recording.\"", "category_id": 1},
        {"term_name": "Tachycardia", "clue1": "Cardiovascular", "clue2": "Racing pulse, palpitations, dizziness", "clue3": "fast/rapid", "clue4": "no extra chunk -- just \"fast\" + \"heart.\"", "category_id": 1},
        {"term_name": "Bradycardia", "clue1": "Cardiovascular", "clue2": "Fatigue, dizziness, fainting", "clue3": "slow", "clue4": "no extra chunk -- just \"slow\" + \"heart.\"", "category_id": 1},
        {"term_name": "Cardiovascular", "clue1": "Cardiovascular", "clue2": "N/A -- a descriptive term", "clue3": "relating to", "clue4": "contains a chunk meaning \"vessel\" -- relating to the heart AND blood ______.", "category_id": 1},
        {"term_name": "Cardiomegaly", "clue1": "Cardiovascular", "clue2": "Shortness of breath, swelling, fatigue", "clue3": "enlargement", "clue4": "no extra chunk -- just \"heart\" + \"enlargement.\"", "category_id": 1},
        {"term_name": "Pericarditis", "clue1": "Cardiovascular", "clue2": "Sharp chest pain, worse when lying down", "clue3": "inflammation", "clue4": "contains a chunk meaning \"around/surrounding\" -- inflammation of the tissue ______ the heart.", "category_id": 1},
        {"term_name": "Cardiotoxic", "clue1": "Cardiovascular", "clue2": "Irregular heartbeat, heart damage from a substance", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"heart\" + \"poisonous.\"", "category_id": 1},
        {"term_name": "Endocarditis", "clue1": "Cardiovascular", "clue2": "Fever, fatigue, new heart murmur", "clue3": "inflammation", "clue4": "contains a chunk meaning \"inner/within\" -- inflammation of the ______ lining of the heart.", "category_id": 1},
    
        # category_id 2 (Digestive)
        {"term_name": "Gastritis", "clue1": "Digestive", "clue2": "Stomach pain, nausea, bloating", "clue3": "inflammation", "clue4": "no extra chunk -- just \"stomach\" + \"inflammation.\"", "category_id": 2},
        {"term_name": "Gastroenteritis", "clue1": "Digestive", "clue2": "Diarrhea, vomiting, cramping", "clue3": "inflammation", "clue4": "also contains a chunk meaning \"intestine\" -- inflammation of the stomach AND ______.", "category_id": 2},
        {"term_name": "Gastrectomy", "clue1": "Digestive", "clue2": "N/A -- a surgical procedure", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"stomach\" + \"removal.\"", "category_id": 2},
        {"term_name": "Gastroscopy", "clue1": "Digestive", "clue2": "N/A -- a diagnostic procedure", "clue3": "visual examination", "clue4": "no extra chunk -- just \"stomach\" + \"looking into.\"", "category_id": 2},
        {"term_name": "Gastrostomy", "clue1": "Digestive", "clue2": "N/A -- used when a person can't eat normally", "clue3": "creation of a new opening", "clue4": "no extra chunk -- just \"stomach\" + \"new opening.\"", "category_id": 2},
        {"term_name": "Gastroenterology", "clue1": "Digestive", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "contains a chunk meaning \"intestine\" -- study of the stomach AND ______.", "category_id": 2},
        {"term_name": "Gastralgia", "clue1": "Digestive", "clue2": "Cramping or aching stomach pain", "clue3": "pain", "clue4": "no extra chunk -- just \"stomach\" + \"pain.\"", "category_id": 2},
        {"term_name": "Gastroparesis", "clue1": "Digestive", "clue2": "Feeling full quickly, nausea, bloating after eating", "clue3": "weakness/paralysis", "clue4": "no extra chunk -- just \"stomach\" + \"paralysis.\"", "category_id": 2},
        {"term_name": "Gastric Ulcer", "clue1": "Digestive", "clue2": "Burning pain, bloating, nausea", "clue3": "relating to", "clue4": "no extra chunk -- just \"stomach\" + \"relating to.\"", "category_id": 2},
        {"term_name": "Gastrointestinal Bleed", "clue1": "Digestive", "clue2": "Blood in vomit or stool", "clue3": "relating to", "clue4": "contains a chunk meaning \"intestine\" -- relating to the stomach AND ______.", "category_id": 2},
    
        # category_id 3 (Liver)
        {"term_name": "Hepatitis", "clue1": "Digestive (liver)", "clue2": "Jaundice, fatigue, abdominal pain", "clue3": "inflammation", "clue4": "no extra chunk -- just \"liver\" + \"inflammation.\"", "category_id": 3},
        {"term_name": "Hepatomegaly", "clue1": "Digestive (liver)", "clue2": "Abdominal fullness/discomfort, felt on exam", "clue3": "enlargement", "clue4": "no extra chunk -- just \"liver\" + \"enlargement.\"", "category_id": 3},
        {"term_name": "Hepatectomy", "clue1": "Digestive (liver)", "clue2": "N/A -- a surgical procedure", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"liver\" + \"removal.\"", "category_id": 3},
        {"term_name": "Hepatotoxic", "clue1": "Digestive (liver)", "clue2": "Liver damage caused by a substance/drug", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"liver\" + \"poisonous.\"", "category_id": 3},
        {"term_name": "Hepatic Failure", "clue1": "Digestive (liver)", "clue2": "Jaundice, confusion, easy bruising", "clue3": "relating to", "clue4": "no extra chunk -- just \"liver\" + \"relating to.\"", "category_id": 3},
        {"term_name": "Hepatoma", "clue1": "Digestive (liver)", "clue2": "Abdominal mass, weight loss, jaundice", "clue3": "tumor/mass", "clue4": "no extra chunk -- just \"liver\" + \"tumor.\"", "category_id": 3},
        {"term_name": "Hepatology", "clue1": "Digestive (liver)", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"liver\" + \"study of.\"", "category_id": 3},
        {"term_name": "Hepatocyte", "clue1": "Digestive (liver)", "clue2": "N/A -- a type of cell", "clue3": "cell", "clue4": "no extra chunk -- just \"liver\" + \"cell.\"", "category_id": 3},
        {"term_name": "Hepatorenal Syndrome", "clue1": "Digestive & Urinary", "clue2": "Decreased urine output in someone with liver disease", "clue3": "relating to", "clue4": "contains a second organ root meaning \"kidney\" -- relating to the liver AND ______.", "category_id": 3},
    
        # category_id 4 (Urinary)
        {"term_name": "Nephritis", "clue1": "Urinary", "clue2": "Swelling, blood in urine, high blood pressure", "clue3": "inflammation", "clue4": "no extra chunk -- just \"kidney\" + \"inflammation.\"", "category_id": 4},
        {"term_name": "Nephrology", "clue1": "Urinary", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"kidney\" + \"study of.\"", "category_id": 4},
        {"term_name": "Nephrectomy", "clue1": "Urinary", "clue2": "N/A -- a surgical procedure", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"kidney\" + \"removal.\"", "category_id": 4},
        {"term_name": "Nephrotic Syndrome", "clue1": "Urinary", "clue2": "Swelling (especially face/legs), foamy urine", "clue3": "pertaining to/condition of", "clue4": "no extra chunk -- just \"kidney\" + \"pertaining to.\"", "category_id": 4},
        {"term_name": "Renal Failure", "clue1": "Urinary", "clue2": "Fatigue, swelling, decreased urine output", "clue3": "loss of function", "clue4": "no extra chunk -- just \"kidney\" + \"failure.\"", "category_id": 4},
        {"term_name": "Renal Artery Stenosis", "clue1": "Urinary & Cardiovascular", "clue2": "High blood pressure that's hard to control", "clue3": "relating to", "clue4": "no extra chunk -- just \"kidney\" + \"relating to.\"", "category_id": 4},
        {"term_name": "Nephrolithiasis", "clue1": "Urinary", "clue2": "Severe flank/back pain, blood in urine", "clue3": "condition of/formation of", "clue4": "contains a chunk meaning \"stone\" -- condition of ______ in the kidney.", "category_id": 4},
        {"term_name": "Nephropathy", "clue1": "Urinary", "clue2": "Swelling, protein in urine, fatigue", "clue3": "disease", "clue4": "no extra chunk -- just \"kidney\" + \"disease.\"", "category_id": 4},
        {"term_name": "Nephrostomy", "clue1": "Urinary", "clue2": "N/A -- used to drain urine directly from the kidney", "clue3": "creation of a new opening", "clue4": "no extra chunk -- just \"kidney\" + \"new opening.\"", "category_id": 4},
        {"term_name": "Renogram", "clue1": "Urinary", "clue2": "N/A -- a diagnostic scan", "clue3": "a recording/image", "clue4": "no extra chunk -- just \"kidney\" + \"recording.\"", "category_id": 4},
    
        # category_id 5 (Nervous)
        {"term_name": "Neurology", "clue1": "Nervous", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"nerve\" + \"study of.\"", "category_id": 5},
        {"term_name": "Neuropathy", "clue1": "Nervous", "clue2": "Numbness, tingling, weakness (often hands/feet)", "clue3": "disease/disorder", "clue4": "no extra chunk -- just \"nerve\" + \"disease.\"", "category_id": 5},
        {"term_name": "Neuralgia", "clue1": "Nervous", "clue2": "Sharp, shooting pain along a nerve pathway", "clue3": "pain", "clue4": "no extra chunk -- just \"nerve\" + \"pain.\"", "category_id": 5},
        {"term_name": "Neurosurgeon", "clue1": "Nervous", "clue2": "N/A -- a medical specialist", "clue3": "one who performs surgery", "clue4": "no extra chunk -- just \"nerve\" + \"surgeon.\"", "category_id": 5},
        {"term_name": "Neuritis", "clue1": "Nervous", "clue2": "Pain, tingling, numbness", "clue3": "inflammation", "clue4": "no extra chunk -- just \"nerve\" + \"inflammation.\"", "category_id": 5},
        {"term_name": "Neuroma", "clue1": "Nervous", "clue2": "Pain, numbness, a lump-like sensation", "clue3": "tumor/mass", "clue4": "no extra chunk -- just \"nerve\" + \"tumor.\"", "category_id": 5},
        {"term_name": "Neurotransmitter", "clue1": "Nervous", "clue2": "N/A -- a normal body chemical", "clue3": "something that sends/carries across", "clue4": "no extra chunk -- just \"nerve\" + \"carrier chemical.\"", "category_id": 5},
        {"term_name": "Neurotoxic", "clue1": "Nervous", "clue2": "Confusion, seizures, numbness from a substance", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"nerve\" + \"poisonous.\"", "category_id": 5},
        {"term_name": "Polyneuropathy", "clue1": "Nervous", "clue2": "Widespread numbness/weakness in hands and feet", "clue3": "disease", "clue4": "contains a chunk meaning \"many\" -- disease of ______ nerves at once.", "category_id": 5},
    
        # category_id 6 (Skeletal)
        {"term_name": "Osteoporosis", "clue1": "Skeletal", "clue2": "Fractures from minor falls, height loss, stooped posture", "clue3": "porous condition", "clue4": "no extra chunk -- just \"bone\" + \"porous condition.\"", "category_id": 6},
        {"term_name": "Osteoarthritis", "clue1": "Skeletal", "clue2": "Joint pain, stiffness, reduced range of motion", "clue3": "inflammation", "clue4": "contains a chunk meaning \"joint\" -- inflammation of the bone AND ______.", "category_id": 6},
        {"term_name": "Osteomyelitis", "clue1": "Skeletal", "clue2": "Bone pain, fever, swelling/redness over a bone", "clue3": "inflammation", "clue4": "contains a chunk meaning \"marrow\" -- inflammation of the bone AND its ______.", "category_id": 6},
        {"term_name": "Osteopathy", "clue1": "Skeletal", "clue2": "N/A -- a treatment field, or general bone disease", "clue3": "disease/treatment of", "clue4": "no extra chunk -- just \"bone\" + \"disease/treatment.\"", "category_id": 6},
        {"term_name": "Osteoblast", "clue1": "Skeletal", "clue2": "N/A -- a type of cell", "clue3": "immature/building cell", "clue4": "no extra chunk -- just \"bone\" + \"building cell.\"", "category_id": 6},
        {"term_name": "Osteoclast", "clue1": "Skeletal", "clue2": "N/A -- a type of cell", "clue3": "breaking-down cell", "clue4": "no extra chunk -- just \"bone\" + \"breaking-down cell.\"", "category_id": 6},
        {"term_name": "Osteotomy", "clue1": "Skeletal", "clue2": "N/A -- a surgical procedure", "clue3": "surgical cutting", "clue4": "no extra chunk -- just \"bone\" + \"cutting.\"", "category_id": 6},
        {"term_name": "Osteosarcoma", "clue1": "Skeletal", "clue2": "Bone pain, swelling, a mass", "clue3": "a type of cancer", "clue4": "no extra chunk -- just \"bone\" + \"cancer.\"", "category_id": 6},
        {"term_name": "Osteopenia", "clue1": "Skeletal", "clue2": "N/A -- usually found on a bone density scan", "clue3": "deficiency/lack of", "clue4": "no extra chunk -- just \"bone\" + \"deficiency.\"", "category_id": 6},
        {"term_name": "Osteogenesis", "clue1": "Skeletal", "clue2": "N/A -- a normal or genetic process (e.g. fragile bones)", "clue3": "formation/creation of", "clue4": "no extra chunk -- just \"bone\" + \"formation.\"", "category_id": 6},
    
        # category_id 7 (Integumentary)
        {"term_name": "Dermatitis", "clue1": "Integumentary", "clue2": "Redness, itching, rash", "clue3": "inflammation", "clue4": "no extra chunk -- just \"skin\" + \"inflammation.\"", "category_id": 7},
        {"term_name": "Dermatology", "clue1": "Integumentary", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"skin\" + \"study of.\"", "category_id": 7},
        {"term_name": "Dermatosis", "clue1": "Integumentary", "clue2": "Various abnormal skin changes", "clue3": "abnormal condition", "clue4": "no extra chunk -- just \"skin\" + \"abnormal condition.\"", "category_id": 7},
        {"term_name": "Dermatophyte Infection", "clue1": "Integumentary", "clue2": "Itchy, scaly, ring-shaped rash", "clue3": "plant/fungus", "clue4": "no extra chunk -- just \"skin\" + \"fungus.\"", "category_id": 7},
        {"term_name": "Dermabrasion", "clue1": "Integumentary", "clue2": "N/A -- a cosmetic/surgical procedure", "clue3": "wearing away/scraping", "clue4": "no extra chunk -- just \"skin\" + \"scraping away.\"", "category_id": 7},
        {"term_name": "Dermatome", "clue1": "Integumentary & Nervous", "clue2": "N/A -- a nerve-supplied skin zone, or a cutting tool", "clue3": "cutting instrument OR section", "clue4": "no extra chunk -- just \"skin\" + \"cutting/section.\"", "category_id": 7},
        {"term_name": "Dermatomyositis", "clue1": "Integumentary & Muscular", "clue2": "Skin rash plus muscle weakness", "clue3": "inflammation", "clue4": "contains a chunk meaning \"muscle\" -- inflammation of the skin AND ______.", "category_id": 7},
        {"term_name": "Dermatopathology", "clue1": "Integumentary", "clue2": "N/A -- a field of study", "clue3": "study of disease", "clue4": "contains a chunk meaning \"disease\" -- study of skin ______.", "category_id": 7},
        {"term_name": "Epidermis", "clue1": "Integumentary", "clue2": "N/A -- an anatomical structure", "clue3": "upon/above", "clue4": "no extra chunk -- just \"upon\" + \"skin.\"", "category_id": 7},
    
        # category_id 8 (Respiratory)
        {"term_name": "Pulmonary Function Test", "clue1": "Respiratory", "clue2": "N/A -- a descriptive term/diagnostic test", "clue3": "relating to", "clue4": "no extra chunk -- just \"lung\" + \"relating to.\"", "category_id": 8},
        {"term_name": "Pulmonology", "clue1": "Respiratory", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"lung\" + \"study of.\"", "category_id": 8},
        {"term_name": "Pulmonary Embolism", "clue1": "Respiratory & Cardiovascular", "clue2": "Sudden chest pain, difficulty breathing, rapid heart rate", "clue3": "a blockage that traveled from elsewhere", "clue4": "no extra chunk -- just \"lung\" + \"blockage.\"", "category_id": 8},
        {"term_name": "Pulmonary Edema", "clue1": "Respiratory", "clue2": "Severe shortness of breath, wheezing, frothy cough", "clue3": "swelling/fluid buildup", "clue4": "no extra chunk -- just \"lung\" + \"fluid buildup.\"", "category_id": 8},
        {"term_name": "Pulmonary Fibrosis", "clue1": "Respiratory", "clue2": "Dry cough, progressive shortness of breath", "clue3": "scarring/thickening of tissue", "clue4": "no extra chunk -- just \"lung\" + \"scarring.\"", "category_id": 8},
        {"term_name": "Pulmonary Hypertension", "clue1": "Respiratory & Cardiovascular", "clue2": "Shortness of breath, chest pain, fatigue", "clue3": "high blood pressure", "clue4": "no extra chunk -- just \"lung\" + \"high pressure.\"", "category_id": 8},
        {"term_name": "Cardiopulmonary Resuscitation", "clue1": "Cardiovascular & Respiratory", "clue2": "N/A -- an emergency-procedure term", "clue3": "relating to", "clue4": "contains a chunk meaning \"heart\" -- relating to the ______ AND lungs.", "category_id": 8},
        {"term_name": "Pulmonary Artery", "clue1": "Respiratory & Cardiovascular", "clue2": "N/A -- an anatomical structure", "clue3": "a vessel carrying blood", "clue4": "no extra chunk -- just \"lung\" + \"artery.\"", "category_id": 8},
    
        # category_id 9 (Circulatory)
        {"term_name": "Hematology", "clue1": "Blood/Circulatory", "clue2": "N/A -- a field of study", "clue3": "study of", "clue4": "no extra chunk -- just \"blood\" + \"study of.\"", "category_id": 9},
        {"term_name": "Hemoglobin", "clue1": "Blood/Circulatory", "clue2": "N/A -- a protein; low levels cause fatigue/paleness", "clue3": "a globular protein", "clue4": "no extra chunk -- just \"blood\" + \"protein.\"", "category_id": 9},
        {"term_name": "Hematoma", "clue1": "Blood/Circulatory", "clue2": "Swelling, bruising, localized pain after injury", "clue3": "mass/collection of", "clue4": "no extra chunk -- just \"blood\" + \"mass.\"", "category_id": 9},
        {"term_name": "Hemorrhage", "clue1": "Blood/Circulatory", "clue2": "Sudden, excessive, uncontrolled bleeding", "clue3": "bursting forth/excessive flow", "clue4": "no extra chunk -- just \"blood\" + \"bursting forth.\"", "category_id": 9},
        {"term_name": "Hemophilia", "clue1": "Blood/Circulatory", "clue2": "Excessive bleeding, easy bruising, joint bleeding", "clue3": "tendency toward", "clue4": "no extra chunk -- just \"blood\" + \"tendency toward.\"", "category_id": 9},
        {"term_name": "Hemolysis", "clue1": "Blood/Circulatory", "clue2": "Fatigue, jaundice, dark urine", "clue3": "breakdown/destruction", "clue4": "no extra chunk -- just \"blood\" + \"breakdown.\"", "category_id": 9},
        {"term_name": "Hemostasis", "clue1": "Blood/Circulatory", "clue2": "N/A -- a normal body process, not a disease", "clue3": "stopping/controlling", "clue4": "no extra chunk -- just \"blood\" + \"stopping.\"", "category_id": 9},
        {"term_name": "Hematuria", "clue1": "Blood & Urinary", "clue2": "Visible red/pink or cola-colored urine", "clue3": "condition of urine", "clue4": "no extra chunk -- just \"blood\" + \"urine condition.\"", "category_id": 9},
        {"term_name": "Anemia", "clue1": "Blood/Circulatory", "clue2": "Fatigue, pale skin, weakness", "clue3": "without/lack of", "clue4": "no extra chunk -- just \"without\" + \"blood\" (lack of healthy red blood cells).", "category_id": 9},
        {"term_name": "Hemodialysis", "clue1": "Blood & Urinary", "clue2": "N/A -- a treatment for kidney failure", "clue3": "separation/filtering", "clue4": "no extra chunk -- just \"blood\" + \"filtering.\"", "category_id": 9},
    ]

    for category in categoryDict.values():
        session.add(category)

    for term in termsData:
        termIter = Term(term_name=term["term_name"], clue1=term["clue1"], clue2=term["clue2"], clue3=term["clue3"], clue4=term["clue4"], category_id=term["category_id"])
        session.add(termIter)
    
    session.commit()
    
    
