"""
model.py

Defines the SQLAlchemy 2.0 (typed Mapped/mapped_column style) models for
the Next Dr.? game.

Models:
- Category: stores each medical specialty (e.g. Cardiovascular, Digestive, etc.)
- Term: stores each medical term and its 4 progressive clues (clue1-clue4).
- DailyTerm: stores the term of the day for each date (date is unique).
- Visitor: stores each visitor's unique ID, first_seen date, last_seen date, and 
  visitCount.

engine: SQLAlchemy engine connecting to Postgres via .env config.
getTodaysTerm(session): returns the term of the day (deterministic by date).
"""


from sqlalchemy import create_engine, String, Text, select, ForeignKey, func, Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped
from datetime import time, date as dt_date, datetime
from dotenv import load_dotenv
import random
import uuid

import os

load_dotenv()
NEON_URL = os.getenv("NEON_URL")
engine = create_engine(NEON_URL)

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
    specialty: Mapped[str] = mapped_column()

class DailyTerm(Base):
    __tablename__ = "dailyterm"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[dt_date] = mapped_column()
    term_id: Mapped[int] = mapped_column(ForeignKey("term.id"))

class Visitor(Base):
    __tablename__ = "visitors"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    first_seen: Mapped[dt_date] = mapped_column(DateTime, default=lambda: datetime.now())
    last_seen: Mapped[dt_date] = mapped_column(DateTime, default=lambda: datetime.now())
    visitCount: Mapped[int] = mapped_column(Integer, default=1)

Base.metadata.create_all(engine)

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
    # (Cardiovascular)
    {"term_name": "Cardiology", "clue1": "Cardiovascular", "clue2": "The specialist you'd see for chest pain or an irregular heartbeat", "clue3": "study of", "clue4": "no extra chunk -- just \"heart\" + \"study of.\"", "specialty": "Cardiovascular"},
    {"term_name": "Cardiomyopathy", "clue1": "Cardiovascular", "clue2": "Shortness of breath, fatigue, swelling in legs", "clue3": "disease/condition of", "clue4": "also contains a chunk meaning \"muscle\" -- a disease of the heart ______.", "specialty": "Cardiovascular"},
    {"term_name": "Cardiac Arrest", "clue1": "Cardiovascular", "clue2": "Sudden collapse, no pulse, unresponsive", "clue3": "sudden stopping", "clue4": "no extra chunk -- just \"heart\" + \"stopping.\"", "specialty": "Cardiovascular"},
    {"term_name": "Cardiogram", "clue1": "Cardiovascular", "clue2": "A test that traces electrical activity as wavy lines on paper", "clue3": "a recording/tracing", "clue4": "no extra chunk -- just \"heart\" + \"recording.\"", "specialty": "Cardiovascular"},
    {"term_name": "Tachycardia", "clue1": "Cardiovascular", "clue2": "Racing pulse, palpitations, dizziness", "clue3": "fast/rapid", "clue4": "no extra chunk -- just \"fast\" + \"heart.\"", "specialty": "Cardiovascular"},
    {"term_name": "Bradycardia", "clue1": "Cardiovascular", "clue2": "Fatigue, dizziness, fainting", "clue3": "slow", "clue4": "no extra chunk -- just \"slow\" + \"heart.\"", "specialty": "Cardiovascular"},
    {"term_name": "Cardiovascular", "clue1": "Cardiovascular", "clue2": "Used to describe your heart and blood vessels together, e.g. \"___ health\"", "clue3": "relating to", "clue4": "contains a chunk meaning \"vessel\" -- relating to the heart AND blood ______.", "specialty": "Cardiovascular"},
    {"term_name": "Cardiomegaly", "clue1": "Cardiovascular", "clue2": "Shortness of breath, swelling, fatigue", "clue3": "enlargement", "clue4": "no extra chunk -- just \"heart\" + \"enlargement.\"", "specialty": "Cardiovascular"},
    {"term_name": "Pericarditis", "clue1": "Cardiovascular", "clue2": "Sharp chest pain, worse when lying down", "clue3": "inflammation", "clue4": "contains a chunk meaning \"around/surrounding\" -- inflammation of the tissue ______ the heart.", "specialty": "Cardiovascular"},
    {"term_name": "Cardiotoxic", "clue1": "Cardiovascular", "clue2": "Irregular heartbeat, heart damage from a substance", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"heart\" + \"poisonous.\"", "specialty": "Cardiovascular"},
    {"term_name": "Endocarditis", "clue1": "Cardiovascular", "clue2": "Fever, fatigue, new heart murmur", "clue3": "inflammation", "clue4": "contains a chunk meaning \"inner/within\" -- inflammation of the ______ lining of the heart.", "specialty": "Cardiovascular"},

    # 2 (Digestive)
    {"term_name": "Gastritis", "clue1": "Digestive", "clue2": "Stomach pain, nausea, bloating", "clue3": "inflammation", "clue4": "no extra chunk -- just \"stomach\" + \"inflammation.\"", "specialty": "Digestive"},
    {"term_name": "Gastroenteritis", "clue1": "Digestive", "clue2": "Diarrhea, vomiting, cramping", "clue3": "inflammation", "clue4": "also contains a chunk meaning \"intestine\" -- inflammation of the stomach AND ______.", "specialty": "Digestive"},
    {"term_name": "Gastrectomy", "clue1": "Digestive", "clue2": "Sometimes done to treat severe ulcers or stomach cancer", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"stomach\" + \"removal.\"", "specialty": "Digestive"},
    {"term_name": "Gastroscopy", "clue1": "Digestive", "clue2": "A thin camera is passed down the throat for this procedure", "clue3": "visual examination", "clue4": "no extra chunk -- just \"stomach\" + \"looking into.\"", "specialty": "Digestive"},
    {"term_name": "Gastrostomy", "clue1": "Digestive", "clue2": "N/A -- used when a person can't eat normally", "clue3": "creation of a new opening", "clue4": "no extra chunk -- just \"stomach\" + \"new opening.\"", "specialty": "Digestive"},
    {"term_name": "Gastroenterology", "clue1": "Digestive", "clue2": "The specialist you'd see for chronic heartburn, ulcers, or IBS", "clue3": "study of", "clue4": "contains a chunk meaning \"intestine\" -- study of the stomach AND ______.", "specialty": "Digestive"},
    {"term_name": "Gastralgia", "clue1": "Digestive", "clue2": "Cramping or aching stomach pain", "clue3": "pain", "clue4": "no extra chunk -- just \"stomach\" + \"pain.\"", "specialty": "Digestive"},
    {"term_name": "Gastroparesis", "clue1": "Digestive", "clue2": "Feeling full quickly, nausea, bloating after eating", "clue3": "weakness/paralysis", "clue4": "no extra chunk -- just \"stomach\" + \"paralysis.\"", "specialty": "Digestive"},
    {"term_name": "Gastric Ulcer", "clue1": "Digestive", "clue2": "Burning pain, bloating, nausea", "clue3": "relating to", "clue4": "no extra chunk -- just \"stomach\" + \"relating to.\"", "specialty": "Digestive"},
    {"term_name": "Gastrointestinal Bleed", "clue1": "Digestive", "clue2": "Blood in vomit or stool", "clue3": "relating to", "clue4": "contains a chunk meaning \"intestine\" -- relating to the stomach AND ______.", "specialty": "Digestive"},

    # 3 (Liver)
    {"term_name": "Hepatitis", "clue1": "Digestive (liver)", "clue2": "Jaundice, fatigue, abdominal pain", "clue3": "inflammation", "clue4": "no extra chunk -- just \"liver\" + \"inflammation.\"", "specialty": "Liver"},
    {"term_name": "Hepatomegaly", "clue1": "Digestive (liver)", "clue2": "Abdominal fullness/discomfort, felt on exam", "clue3": "enlargement", "clue4": "no extra chunk -- just \"liver\" + \"enlargement.\"", "specialty": "Liver"},
    {"term_name": "Hepatectomy", "clue1": "Digestive (liver)", "clue2": "Can involve removing part of the organ, e.g. for a tumor or donation", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"liver\" + \"removal.\"", "specialty": "Liver"},
    {"term_name": "Hepatotoxic", "clue1": "Digestive (liver)", "clue2": "Liver damage caused by a substance/drug", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"liver\" + \"poisonous.\"", "specialty": "Liver"},
    {"term_name": "Hepatic Failure", "clue1": "Digestive (liver)", "clue2": "Jaundice, confusion, easy bruising", "clue3": "relating to", "clue4": "no extra chunk -- just \"liver\" + \"relating to.\"", "specialty": "Liver"},
    {"term_name": "Hepatoma", "clue1": "Digestive (liver)", "clue2": "Abdominal mass, weight loss, jaundice", "clue3": "tumor/mass", "clue4": "no extra chunk -- just \"liver\" + \"tumor.\"", "specialty": "Liver"},
    {"term_name": "Hepatology", "clue1": "Digestive (liver)", "clue2": "The specialist you'd see for hepatitis or cirrhosis", "clue3": "study of", "clue4": "no extra chunk -- just \"liver\" + \"study of.\"", "specialty": "Liver"},
    {"term_name": "Hepatocyte", "clue1": "Digestive (liver)", "clue2": "The main functional cell type making up this organ's tissue", "clue3": "cell", "clue4": "no extra chunk -- just \"liver\" + \"cell.\"", "specialty": "Liver"},
    {"term_name": "Hepatorenal Syndrome", "clue1": "Digestive & Urinary", "clue2": "Decreased urine output in someone with liver disease", "clue3": "relating to", "clue4": "contains a second organ root meaning \"kidney\" -- relating to the liver AND ______.", "specialty": "Liver"},

    # 4 (Urinary)
    {"term_name": "Nephritis", "clue1": "Urinary", "clue2": "Swelling, blood in urine, high blood pressure", "clue3": "inflammation", "clue4": "no extra chunk -- just \"kidney\" + \"inflammation.\"", "specialty": "Urinary"},
    {"term_name": "Nephrology", "clue1": "Urinary", "clue2": "The specialist you'd see for chronic kidney disease", "clue3": "study of", "clue4": "no extra chunk -- just \"kidney\" + \"study of.\"", "specialty": "Urinary"},
    {"term_name": "Nephrectomy", "clue1": "Urinary", "clue2": "Often done to treat kidney cancer or for organ donation", "clue3": "surgical removal", "clue4": "no extra chunk -- just \"kidney\" + \"removal.\"", "specialty": "Urinary"},
    {"term_name": "Nephrotic Syndrome", "clue1": "Urinary", "clue2": "Swelling (especially face/legs), foamy urine", "clue3": "pertaining to/condition of", "clue4": "no extra chunk -- just \"kidney\" + \"pertaining to.\"", "specialty": "Urinary"},
    {"term_name": "Renal Failure", "clue1": "Urinary", "clue2": "Fatigue, swelling, decreased urine output", "clue3": "loss of function", "clue4": "no extra chunk -- just \"kidney\" + \"failure.\"", "specialty": "Urinary"},
    {"term_name": "Renal Artery Stenosis", "clue1": "Urinary & Cardiovascular", "clue2": "High blood pressure that's hard to control", "clue3": "relating to", "clue4": "no extra chunk -- just \"kidney\" + \"relating to.\"", "specialty": "Urinary"},
    {"term_name": "Nephrolithiasis", "clue1": "Urinary", "clue2": "Severe flank/back pain, blood in urine", "clue3": "condition of/formation of", "clue4": "contains a chunk meaning \"stone\" -- condition of ______ in the kidney.", "specialty": "Urinary"},
    {"term_name": "Nephropathy", "clue1": "Urinary", "clue2": "Swelling, protein in urine, fatigue", "clue3": "disease", "clue4": "no extra chunk -- just \"kidney\" + \"disease.\"", "specialty": "Urinary"},
    {"term_name": "Nephrostomy", "clue1": "Urinary", "clue2": "N/A -- used to drain urine directly from the kidney", "clue3": "creation of a new opening", "clue4": "no extra chunk -- just \"kidney\" + \"new opening.\"", "specialty": "Urinary"},
    {"term_name": "Renogram", "clue1": "Urinary", "clue2": "A nuclear medicine scan that shows how well each kidney filters blood", "clue3": "a recording/image", "clue4": "no extra chunk -- just \"kidney\" + \"recording.\"", "specialty": "Urinary"},

    # 5 (Nervous)
    {"term_name": "Neurology", "clue1": "Nervous", "clue2": "The specialist you'd see for seizures or migraines", "clue3": "study of", "clue4": "no extra chunk -- just \"nerve\" + \"study of.\"", "specialty": "Nervous"},
    {"term_name": "Neuropathy", "clue1": "Nervous", "clue2": "Numbness, tingling, weakness (often hands/feet)", "clue3": "disease/disorder", "clue4": "no extra chunk -- just \"nerve\" + \"disease.\"", "specialty": "Nervous"},
    {"term_name": "Neuralgia", "clue1": "Nervous", "clue2": "Sharp, shooting pain along a nerve pathway", "clue3": "pain", "clue4": "no extra chunk -- just \"nerve\" + \"pain.\"", "specialty": "Nervous"},
    {"term_name": "Neurosurgeon", "clue1": "Nervous", "clue2": "Operates on the brain and spinal cord", "clue3": "one who performs surgery", "clue4": "no extra chunk -- just \"nerve\" + \"surgeon.\"", "specialty": "Nervous"},
    {"term_name": "Neuritis", "clue1": "Nervous", "clue2": "Pain, tingling, numbness", "clue3": "inflammation", "clue4": "no extra chunk -- just \"nerve\" + \"inflammation.\"", "specialty": "Nervous"},
    {"term_name": "Neuroma", "clue1": "Nervous", "clue2": "Pain, numbness, a lump-like sensation", "clue3": "tumor/mass", "clue4": "no extra chunk -- just \"nerve\" + \"tumor.\"", "specialty": "Nervous"},
    {"term_name": "Neurotransmitter", "clue1": "Nervous", "clue2": "Dopamine and serotonin are examples of this type of chemical", "clue3": "something that sends/carries across", "clue4": "no extra chunk -- just \"nerve\" + \"carrier chemical.\"", "specialty": "Nervous"},
    {"term_name": "Neurotoxic", "clue1": "Nervous", "clue2": "Confusion, seizures, numbness from a substance", "clue3": "poisonous/harmful to", "clue4": "no extra chunk -- just \"nerve\" + \"poisonous.\"", "specialty": "Nervous"},
    {"term_name": "Polyneuropathy", "clue1": "Nervous", "clue2": "Widespread numbness/weakness in hands and feet", "clue3": "disease", "clue4": "contains a chunk meaning \"many\" -- disease of ______ nerves at once.", "specialty": "Nervous"},

    # 6 (Skeletal)
    {"term_name": "Osteoporosis", "clue1": "Skeletal", "clue2": "Fractures from minor falls, height loss, stooped posture", "clue3": "porous condition", "clue4": "no extra chunk -- just \"bone\" + \"porous condition.\"", "specialty": "Skeletal"},
    {"term_name": "Osteoarthritis", "clue1": "Skeletal", "clue2": "Joint pain, stiffness, reduced range of motion", "clue3": "inflammation", "clue4": "contains a chunk meaning \"joint\" -- inflammation of the bone AND ______.", "specialty": "Skeletal"},
    {"term_name": "Osteomyelitis", "clue1": "Skeletal", "clue2": "Bone pain, fever, swelling/redness over a bone", "clue3": "inflammation", "clue4": "contains a chunk meaning \"marrow\" -- inflammation of the bone AND its ______.", "specialty": "Skeletal"},
    {"term_name": "Osteopathy", "clue1": "Skeletal", "clue2": "Some practitioners use hands-on manipulation as part of this approach", "clue3": "disease/treatment of", "clue4": "no extra chunk -- just \"bone\" + \"disease/treatment.\"", "specialty": "Skeletal"},
    {"term_name": "Osteoblast", "clue1": "Skeletal", "clue2": "This cell type lays down new bone tissue", "clue3": "immature/building cell", "clue4": "no extra chunk -- just \"bone\" + \"building cell.\"", "specialty": "Skeletal"},
    {"term_name": "Osteoclast", "clue1": "Skeletal", "clue2": "This cell type breaks down old bone tissue during remodeling", "clue3": "breaking-down cell", "clue4": "no extra chunk -- just \"bone\" + \"breaking-down cell.\"", "specialty": "Skeletal"},
    {"term_name": "Osteotomy", "clue1": "Skeletal", "clue2": "A bone is deliberately cut and repositioned, often to correct alignment", "clue3": "surgical cutting", "clue4": "no extra chunk -- just \"bone\" + \"cutting.\"", "specialty": "Skeletal"},
    {"term_name": "Osteosarcoma", "clue1": "Skeletal", "clue2": "Bone pain, swelling, a mass", "clue3": "a type of cancer", "clue4": "no extra chunk -- just \"bone\" + \"cancer.\"", "specialty": "Skeletal"},
    {"term_name": "Osteopenia", "clue1": "Skeletal", "clue2": "Milder than osteoporosis, often caught early on a bone density scan", "clue3": "deficiency/lack of", "clue4": "no extra chunk -- just \"bone\" + \"deficiency.\"", "specialty": "Skeletal"},
    {"term_name": "Osteogenesis", "clue1": "Skeletal", "clue2": "A normal process, but \"___ Imperfecta\" is a genetic brittle-bone disease", "clue3": "formation/creation of", "clue4": "no extra chunk -- just \"bone\" + \"formation.\"", "specialty": "Skeletal"},

    # 7 (Integumentary)
    {"term_name": "Dermatitis", "clue1": "Integumentary", "clue2": "Redness, itching, rash", "clue3": "inflammation", "clue4": "no extra chunk -- just \"skin\" + \"inflammation.\"", "specialty": "Integumentary"},
    {"term_name": "Dermatology", "clue1": "Integumentary", "clue2": "The specialist you'd see for acne, eczema, or a suspicious mole", "clue3": "study of", "clue4": "no extra chunk -- just \"skin\" + \"study of.\"", "specialty": "Integumentary"},
    {"term_name": "Dermatosis", "clue1": "Integumentary", "clue2": "Various abnormal skin changes", "clue3": "abnormal condition", "clue4": "no extra chunk -- just \"skin\" + \"abnormal condition.\"", "specialty": "Integumentary"},
    {"term_name": "Dermatophyte Infection", "clue1": "Integumentary", "clue2": "Itchy, scaly, ring-shaped rash", "clue3": "plant/fungus", "clue4": "no extra chunk -- just \"skin\" + \"fungus.\"", "specialty": "Integumentary"},
    {"term_name": "Dermabrasion", "clue1": "Integumentary", "clue2": "A cosmetic procedure that removes the top skin layer to reduce scarring", "clue3": "wearing away/scraping", "clue4": "no extra chunk -- just \"skin\" + \"scraping away.\"", "specialty": "Integumentary"},
    {"term_name": "Dermatome", "clue1": "Integumentary & Nervous", "clue2": "Also refers to a skin area supplied by a single spinal nerve", "clue3": "cutting instrument OR section", "clue4": "no extra chunk -- just \"skin\" + \"cutting/section.\"", "specialty": "Integumentary"},
    {"term_name": "Dermatomyositis", "clue1": "Integumentary & Muscular", "clue2": "Skin rash plus muscle weakness", "clue3": "inflammation", "clue4": "contains a chunk meaning \"muscle\" -- inflammation of the skin AND ______.", "specialty": "Integumentary"},
    {"term_name": "Dermatopathology", "clue1": "Integumentary", "clue2": "Combines skin medicine with examining tissue samples under a microscope", "clue3": "study of disease", "clue4": "contains a chunk meaning \"disease\" -- study of skin ______.", "specialty": "Integumentary"},
    {"term_name": "Epidermis", "clue1": "Integumentary", "clue2": "The outermost layer you can actually see and touch", "clue3": "upon/above", "clue4": "no extra chunk -- just \"upon\" + \"skin.\"", "specialty": "Integumentary"},

    # 8 (Respiratory)
    {"term_name": "Pulmonary Function Test", "clue1": "Respiratory", "clue2": "Measures how much air you can breathe in and out, and how fast", "clue3": "relating to", "clue4": "no extra chunk -- just \"lung\" + \"relating to.\"", "specialty": "Respiratory"},
    {"term_name": "Pulmonology", "clue1": "Respiratory", "clue2": "The specialist you'd see for asthma or COPD", "clue3": "study of", "clue4": "no extra chunk -- just \"lung\" + \"study of.\"", "specialty": "Respiratory"},
    {"term_name": "Pulmonary Embolism", "clue1": "Respiratory & Cardiovascular", "clue2": "Sudden chest pain, difficulty breathing, rapid heart rate", "clue3": "a blockage that traveled from elsewhere", "clue4": "no extra chunk -- just \"lung\" + \"blockage.\"", "specialty": "Respiratory"},
    {"term_name": "Pulmonary Edema", "clue1": "Respiratory", "clue2": "Severe shortness of breath, wheezing, frothy cough", "clue3": "swelling/fluid buildup", "clue4": "no extra chunk -- just \"lung\" + \"fluid buildup.\"", "specialty": "Respiratory"},
    {"term_name": "Pulmonary Fibrosis", "clue1": "Respiratory", "clue2": "Dry cough, progressive shortness of breath", "clue3": "scarring/thickening of tissue", "clue4": "no extra chunk -- just \"lung\" + \"scarring.\"", "specialty": "Respiratory"},
    {"term_name": "Pulmonary Hypertension", "clue1": "Respiratory & Cardiovascular", "clue2": "Shortness of breath, chest pain, fatigue", "clue3": "high blood pressure", "clue4": "no extra chunk -- just \"lung\" + \"high pressure.\"", "specialty": "Respiratory"},
    {"term_name": "Cardiopulmonary Resuscitation", "clue1": "Cardiovascular & Respiratory", "clue2": "The emergency procedure taught in first-aid classes, using chest compressions", "clue3": "relating to", "clue4": "contains a chunk meaning \"heart\" -- relating to the ______ AND lungs.", "specialty": "Respiratory"},
    {"term_name": "Pulmonary Artery", "clue1": "Respiratory & Cardiovascular", "clue2": "Unusual among arteries -- it carries oxygen-poor blood", "clue3": "a vessel carrying blood", "clue4": "no extra chunk -- just \"lung\" + \"artery.\"", "specialty": "Respiratory"},

    # 9 (Circulatory)
    {"term_name": "Hematology", "clue1": "Blood/Circulatory", "clue2": "The specialist you'd see for anemia or a clotting disorder", "clue3": "study of", "clue4": "no extra chunk -- just \"blood\" + \"study of.\"", "specialty": "Circulatory"},
    {"term_name": "Hemoglobin", "clue1": "Blood/Circulatory", "clue2": "The protein inside red blood cells that carries oxygen", "clue3": "a globular protein", "clue4": "no extra chunk -- just \"blood\" + \"protein.\"", "specialty": "Circulatory"},
    {"term_name": "Hematoma", "clue1": "Blood/Circulatory", "clue2": "Swelling, bruising, localized pain after injury", "clue3": "mass/collection of", "clue4": "no extra chunk -- just \"blood\" + \"mass.\"", "specialty": "Circulatory"},
    {"term_name": "Hemorrhage", "clue1": "Blood/Circulatory", "clue2": "Sudden, excessive, uncontrolled bleeding", "clue3": "bursting forth/excessive flow", "clue4": "no extra chunk -- just \"blood\" + \"bursting forth.\"", "specialty": "Circulatory"},
    {"term_name": "Hemophilia", "clue1": "Blood/Circulatory", "clue2": "Excessive bleeding, easy bruising, joint bleeding", "clue3": "tendency toward", "clue4": "no extra chunk -- just \"blood\" + \"tendency toward.\"", "specialty": "Circulatory"},
    {"term_name": "Hemolysis", "clue1": "Blood/Circulatory", "clue2": "Fatigue, jaundice, dark urine", "clue3": "breakdown/destruction", "clue4": "no extra chunk -- just \"blood\" + \"breakdown.\"", "specialty": "Circulatory"},
    {"term_name": "Hemostasis", "clue1": "Blood/Circulatory", "clue2": "The body's normal process of stopping bleeding after an injury", "clue3": "stopping/controlling", "clue4": "no extra chunk -- just \"blood\" + \"stopping.\"", "specialty": "Circulatory"},
    {"term_name": "Hematuria", "clue1": "Blood & Urinary", "clue2": "Visible red/pink or cola-colored urine", "clue3": "condition of urine", "clue4": "no extra chunk -- just \"blood\" + \"urine condition.\"", "specialty": "Circulatory"},
    {"term_name": "Anemia", "clue1": "Blood/Circulatory", "clue2": "Fatigue, pale skin, weakness", "clue3": "without/lack of", "clue4": "no extra chunk -- just \"without\" + \"blood\" (lack of healthy red blood cells).", "specialty": "Circulatory"},
    {"term_name": "Hemodialysis", "clue1": "Blood & Urinary", "clue2": "A machine filters the blood when the kidneys can no longer do it themselves", "clue3": "separation/filtering", "clue4": "no extra chunk -- just \"blood\" + \"filtering.\"", "specialty": "Circulatory"},
    ]

def getTodaysTerm(session):
    todays_puzzle = session.query(DailyTerm).filter(DailyTerm.date == dt_date.today()).first()
    if todays_puzzle==None:
        todaysNewPuzzle = session.query(Term).order_by(func.random()).first()
        session.add(DailyTerm(date=dt_date.today(), term_id = todaysNewPuzzle.id))
        session.commit()
        return (todaysNewPuzzle)
    else:
        return (session.query(Term).filter(Term.id==todays_puzzle.term_id).first())
    
if __name__ == "__main__":
    with Session(engine) as session:
        session.query(Term).delete()
        session.query(Category).delete()
        session.commit()
        for termDict in termsData:
            session.add(Term(**termDict))
        session.commit()