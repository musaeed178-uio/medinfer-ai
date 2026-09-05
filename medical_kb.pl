% ============================================================
% Medical Expert System - Knowledge Base (SWI-Prolog)
% SPDX-License-Identifier: AGPL-3.0-or-later
%
% The facts block between the BEGIN/END markers below is GENERATED
% from kb_catalog.json by generate_kb.py. Edit kb_catalog.json and
% run `python generate_kb.py`; do not hand-edit that block.
% The header and the inference rules below are maintained by hand.
% ============================================================

:- dynamic patient_has/1, patient_sev/2.

% ------------------- GENERATED FACTS (BEGIN) -------------------
% Knowledge facts generated from kb_catalog.json (version 2.0).
%% Do not edit by hand - regenerate with: python generate_kb.py

% Diseases
disease(flu).
disease(cold).
disease(covid19).
disease(malaria).
disease(dengue).
disease(typhoid).
disease(migraine).
disease(asthma).
disease(pneumonia).
disease(diabetes).
disease(hypertension).
disease(anemia).
disease(allergy).
disease(chickenpox).
disease(measles).
disease(hepatitis_a).
disease(tuberculosis).
disease(bronchitis).
disease(sinusitis).
disease(urinary_tract_infection).
disease(gastroenteritis).
disease(heat_stroke).
disease(insomnia).
disease(depression).
disease(arthritis).

% Disease categories
category(flu, viral).
category(cold, viral).
category(covid19, viral).
category(malaria, parasitic).
category(dengue, viral).
category(typhoid, bacterial).
category(migraine, neurological).
category(asthma, respiratory).
category(pneumonia, respiratory).
category(diabetes, metabolic).
category(hypertension, cardiovascular).
category(anemia, hematologic).
category(allergy, immune).
category(chickenpox, viral).
category(measles, viral).
category(hepatitis_a, viral).
category(tuberculosis, bacterial).
category(bronchitis, respiratory).
category(sinusitis, inflammatory).
category(urinary_tract_infection, bacterial).
category(gastroenteritis, gastrointestinal).
category(heat_stroke, environmental).
category(insomnia, neurological).
category(depression, psychological).
category(arthritis, musculoskeletal).

% Disease descriptions
description(flu, 'Influenza is a viral infection that attacks the respiratory system. It is highly contagious and spreads through droplets.').
description(cold, 'The common cold is a viral infection of the upper respiratory tract. It is usually mild and self-limiting.').
description(covid19, 'COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. It can range from mild to severe and is highly contagious.').
description(malaria, 'Malaria is a parasitic disease transmitted through mosquito bites. It causes recurrent fever and can be life-threatening.').
description(dengue, 'Dengue is a mosquito-borne viral infection causing severe flu-like symptoms and sometimes hemorrhagic fever.').
description(typhoid, 'Typhoid fever is a bacterial infection caused by Salmonella typhi, spread through contaminated food and water.').
description(migraine, 'Migraine is a neurological condition causing intense, debilitating headaches often accompanied by nausea and sensitivity to light.').
description(asthma, 'Asthma is a chronic respiratory condition causing airway inflammation and narrowing, leading to breathing difficulties.').
description(pneumonia, 'Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid.').
description(diabetes, 'Diabetes is a metabolic disorder characterized by high blood sugar levels over a prolonged period.').
description(hypertension, 'Hypertension or high blood pressure is a chronic condition where blood pressure in the arteries is elevated.').
description(anemia, 'Anemia is a condition where the body lacks enough healthy red blood cells to carry adequate oxygen to tissues.').
description(allergy, 'Allergies are immune system reactions to foreign substances that are typically harmless to most people.').
description(chickenpox, 'Chickenpox is a highly contagious viral infection causing an itchy rash with small fluid-filled blisters.').
description(measles, 'Measles is a highly contagious viral infection causing a distinctive red rash, fever, and cough.').
description(hepatitis_a, 'Hepatitis A is a viral liver infection transmitted through contaminated food or water.').
description(tuberculosis, 'Tuberculosis is a bacterial infection that primarily affects the lungs and spreads through airborne droplets.').
description(bronchitis, 'Bronchitis is inflammation of the bronchial tubes, causing persistent cough with mucus.').
description(sinusitis, 'Sinusitis is inflammation of the sinuses, usually caused by infection, leading to facial pain and congestion.').
description(urinary_tract_infection, 'UTI is a bacterial infection in any part of the urinary system, most commonly the bladder.').
description(gastroenteritis, 'Gastroenteritis is inflammation of the stomach and intestines, causing diarrhea and vomiting.').
description(heat_stroke, 'Heat stroke is a severe heat-related illness occurring when body temperature rises rapidly and the body cannot cool down.').
description(insomnia, 'Insomnia is a sleep disorder characterized by difficulty falling or staying asleep.').
description(depression, 'Depression is a mental health disorder causing persistent feelings of sadness and loss of interest.').
description(arthritis, 'Arthritis is inflammation of one or more joints, causing pain and stiffness that worsens with age.').

% Recommendations
recommendation(flu, 'Rest, stay hydrated, take antiviral medications if prescribed, and isolate to prevent spreading.').
recommendation(cold, 'Rest, drink warm fluids, use saline nasal drops, and take over-the-counter cold remedies.').
recommendation(covid19, 'Isolate immediately, monitor oxygen levels, seek medical attention if breathing becomes difficult.').
recommendation(malaria, 'Seek immediate medical treatment, take antimalarial drugs, and use mosquito nets.').
recommendation(dengue, 'Seek medical care, stay hydrated, avoid aspirin, and monitor platelet count.').
recommendation(typhoid, 'Consult a doctor for antibiotics, maintain hygiene, and drink only boiled water.').
recommendation(migraine, 'Rest in a dark room, avoid triggers, take prescribed migraine medication.').
recommendation(asthma, 'Use inhaler as prescribed, avoid triggers, and seek emergency care if breathing worsens.').
recommendation(pneumonia, 'Seek medical attention, take prescribed antibiotics, rest, and stay hydrated.').
recommendation(diabetes, 'Monitor blood sugar regularly, follow a diabetic diet, exercise, and take prescribed medication.').
recommendation(hypertension, 'Reduce salt intake, exercise regularly, manage stress, and take prescribed medication.').
recommendation(anemia, 'Increase iron-rich foods, take iron supplements, and consult a doctor for underlying causes.').
recommendation(allergy, 'Avoid allergens, take antihistamines, and use nasal sprays for relief.').
recommendation(chickenpox, 'Isolate, avoid scratching, use calamine lotion, and take fever reducers.').
recommendation(measles, 'Isolate, rest, stay hydrated, and seek medical care for complications.').
recommendation(hepatitis_a, 'Rest, avoid alcohol, eat a balanced diet, and consult a doctor.').
recommendation(tuberculosis, 'Seek immediate medical treatment, complete full antibiotic course, and isolate initially.').
recommendation(bronchitis, 'Rest, stay hydrated, use a humidifier, and avoid smoke exposure.').
recommendation(sinusitis, 'Use saline nasal irrigation, steam inhalation, and decongestants.').
recommendation(urinary_tract_infection, 'Drink plenty of water, urinate frequently, and take prescribed antibiotics.').
recommendation(gastroenteritis, 'Stay hydrated with oral rehydration solutions, eat bland foods, and rest.').
recommendation(heat_stroke, 'Move to a cool place, apply cold water, seek emergency medical care immediately.').
recommendation(insomnia, 'Maintain regular sleep schedule, avoid screens before bed, and practice relaxation.').
recommendation(depression, 'Seek professional counseling, maintain social connections, and consider therapy.').
recommendation(arthritis, 'Exercise gently, apply heat/cold therapy, and consult a rheumatologist.').

% Emergency flags
is_emergency(covid19).
is_emergency(malaria).
is_emergency(dengue).
is_emergency(pneumonia).
is_emergency(hepatitis_a).
is_emergency(tuberculosis).
is_emergency(heat_stroke).

% Symptoms
symptom(fever).
symptom(fatigue).
symptom(chills).
symptom(sweating).
symptom(weight_loss).
symptom(loss_of_appetite).
symptom(night_sweats).
symptom(cough).
symptom(shortness_of_breath).
symptom(sore_throat).
symptom(wheezing).
symptom(runny_nose).
symptom(nasal_congestion).
symptom(sneezing).
symptom(coughing_blood).
symptom(headache).
symptom(dizziness).
symptom(blurred_vision).
symptom(sensitivity_to_light).
symptom(confusion).
symptom(insomnia).
symptom(difficulty_concentrating).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(abdominal_pain).
symptom(bloating).
symptom(body_ache).
symptom(joint_pain).
symptom(muscle_pain).
symptom(back_pain).
symptom(stiff_joints).
symptom(rash).
symptom(pale_skin).
symptom(yellowing_of_skin).
symptom(chest_pain).
symptom(rapid_heartbeat).
symptom(cold_hands_and_feet).
symptom(frequent_urination).
symptom(burning_urination).
symptom(blood_in_urine).
symptom(sadness).
symptom(loss_of_interest).
symptom(itchy_eyes).
symptom(red_eyes).
symptom(swollen_glands).
symptom(facial_pain).
symptom(increased_thirst).

% Disease-symptom links
has_symptom(flu, fever).
has_symptom(flu, cough).
has_symptom(flu, headache).
has_symptom(flu, fatigue).
has_symptom(flu, body_ache).
has_symptom(flu, chills).
has_symptom(flu, sore_throat).
has_symptom(cold, runny_nose).
has_symptom(cold, sneezing).
has_symptom(cold, sore_throat).
has_symptom(cold, cough).
has_symptom(cold, headache).
has_symptom(cold, fatigue).
has_symptom(cold, nasal_congestion).
has_symptom(covid19, fever).
has_symptom(covid19, cough).
has_symptom(covid19, shortness_of_breath).
has_symptom(covid19, fatigue).
has_symptom(covid19, body_ache).
has_symptom(covid19, headache).
has_symptom(covid19, loss_of_appetite).
has_symptom(covid19, sore_throat).
has_symptom(malaria, fever).
has_symptom(malaria, chills).
has_symptom(malaria, sweating).
has_symptom(malaria, headache).
has_symptom(malaria, nausea).
has_symptom(malaria, vomiting).
has_symptom(malaria, body_ache).
has_symptom(dengue, fever).
has_symptom(dengue, headache).
has_symptom(dengue, joint_pain).
has_symptom(dengue, muscle_pain).
has_symptom(dengue, rash).
has_symptom(dengue, nausea).
has_symptom(dengue, vomiting).
has_symptom(dengue, swollen_glands).
has_symptom(typhoid, fever).
has_symptom(typhoid, headache).
has_symptom(typhoid, fatigue).
has_symptom(typhoid, nausea).
has_symptom(typhoid, vomiting).
has_symptom(typhoid, diarrhea).
has_symptom(typhoid, loss_of_appetite).
has_symptom(typhoid, abdominal_pain).
has_symptom(migraine, headache).
has_symptom(migraine, nausea).
has_symptom(migraine, vomiting).
has_symptom(migraine, blurred_vision).
has_symptom(migraine, dizziness).
has_symptom(migraine, sensitivity_to_light).
has_symptom(asthma, shortness_of_breath).
has_symptom(asthma, wheezing).
has_symptom(asthma, chest_pain).
has_symptom(asthma, cough).
has_symptom(asthma, fatigue).
has_symptom(pneumonia, fever).
has_symptom(pneumonia, cough).
has_symptom(pneumonia, shortness_of_breath).
has_symptom(pneumonia, chest_pain).
has_symptom(pneumonia, fatigue).
has_symptom(pneumonia, chills).
has_symptom(pneumonia, sweating).
has_symptom(pneumonia, nausea).
has_symptom(diabetes, frequent_urination).
has_symptom(diabetes, increased_thirst).
has_symptom(diabetes, fatigue).
has_symptom(diabetes, blurred_vision).
has_symptom(diabetes, weight_loss).
has_symptom(hypertension, headache).
has_symptom(hypertension, dizziness).
has_symptom(hypertension, chest_pain).
has_symptom(hypertension, shortness_of_breath).
has_symptom(hypertension, blurred_vision).
has_symptom(anemia, fatigue).
has_symptom(anemia, pale_skin).
has_symptom(anemia, dizziness).
has_symptom(anemia, shortness_of_breath).
has_symptom(anemia, cold_hands_and_feet).
has_symptom(anemia, headache).
has_symptom(allergy, sneezing).
has_symptom(allergy, itchy_eyes).
has_symptom(allergy, runny_nose).
has_symptom(allergy, rash).
has_symptom(allergy, cough).
has_symptom(allergy, nasal_congestion).
has_symptom(chickenpox, fever).
has_symptom(chickenpox, rash).
has_symptom(chickenpox, fatigue).
has_symptom(chickenpox, headache).
has_symptom(chickenpox, loss_of_appetite).
has_symptom(measles, fever).
has_symptom(measles, rash).
has_symptom(measles, cough).
has_symptom(measles, runny_nose).
has_symptom(measles, red_eyes).
has_symptom(measles, fatigue).
has_symptom(hepatitis_a, fever).
has_symptom(hepatitis_a, fatigue).
has_symptom(hepatitis_a, nausea).
has_symptom(hepatitis_a, vomiting).
has_symptom(hepatitis_a, abdominal_pain).
has_symptom(hepatitis_a, yellowing_of_skin).
has_symptom(hepatitis_a, loss_of_appetite).
has_symptom(tuberculosis, cough).
has_symptom(tuberculosis, fever).
has_symptom(tuberculosis, night_sweats).
has_symptom(tuberculosis, weight_loss).
has_symptom(tuberculosis, fatigue).
has_symptom(tuberculosis, chest_pain).
has_symptom(tuberculosis, coughing_blood).
has_symptom(bronchitis, cough).
has_symptom(bronchitis, fatigue).
has_symptom(bronchitis, chest_pain).
has_symptom(bronchitis, shortness_of_breath).
has_symptom(bronchitis, wheezing).
has_symptom(bronchitis, fever).
has_symptom(sinusitis, facial_pain).
has_symptom(sinusitis, nasal_congestion).
has_symptom(sinusitis, headache).
has_symptom(sinusitis, runny_nose).
has_symptom(sinusitis, fatigue).
has_symptom(sinusitis, fever).
has_symptom(urinary_tract_infection, burning_urination).
has_symptom(urinary_tract_infection, frequent_urination).
has_symptom(urinary_tract_infection, abdominal_pain).
has_symptom(urinary_tract_infection, blood_in_urine).
has_symptom(urinary_tract_infection, fever).
has_symptom(gastroenteritis, diarrhea).
has_symptom(gastroenteritis, vomiting).
has_symptom(gastroenteritis, nausea).
has_symptom(gastroenteritis, abdominal_pain).
has_symptom(gastroenteritis, fever).
has_symptom(gastroenteritis, bloating).
has_symptom(heat_stroke, fever).
has_symptom(heat_stroke, headache).
has_symptom(heat_stroke, dizziness).
has_symptom(heat_stroke, nausea).
has_symptom(heat_stroke, confusion).
has_symptom(heat_stroke, rapid_heartbeat).
has_symptom(insomnia, insomnia).
has_symptom(insomnia, fatigue).
has_symptom(insomnia, headache).
has_symptom(insomnia, difficulty_concentrating).
has_symptom(insomnia, dizziness).
has_symptom(depression, sadness).
has_symptom(depression, loss_of_interest).
has_symptom(depression, fatigue).
has_symptom(depression, insomnia).
has_symptom(depression, difficulty_concentrating).
has_symptom(depression, loss_of_appetite).
has_symptom(arthritis, joint_pain).
has_symptom(arthritis, stiff_joints).
has_symptom(arthritis, fatigue).
has_symptom(arthritis, back_pain).
has_symptom(arthritis, muscle_pain).

% Severity weights (one per disease-symptom pair; symptoms without an
% explicit weight in the catalog default to 1.0)
severity_weight(flu, fever, 1.2).
severity_weight(flu, cough, 1.0).
severity_weight(flu, headache, 1.0).
severity_weight(flu, fatigue, 1.0).
severity_weight(flu, body_ache, 1.1).
severity_weight(flu, chills, 1.0).
severity_weight(flu, sore_throat, 1.0).
severity_weight(cold, runny_nose, 1.0).
severity_weight(cold, sneezing, 1.0).
severity_weight(cold, sore_throat, 1.0).
severity_weight(cold, cough, 1.0).
severity_weight(cold, headache, 1.0).
severity_weight(cold, fatigue, 1.0).
severity_weight(cold, nasal_congestion, 1.0).
severity_weight(covid19, fever, 1.0).
severity_weight(covid19, cough, 1.0).
severity_weight(covid19, shortness_of_breath, 1.5).
severity_weight(covid19, fatigue, 1.0).
severity_weight(covid19, body_ache, 1.0).
severity_weight(covid19, headache, 1.0).
severity_weight(covid19, loss_of_appetite, 1.1).
severity_weight(covid19, sore_throat, 1.0).
severity_weight(malaria, fever, 1.0).
severity_weight(malaria, chills, 1.3).
severity_weight(malaria, sweating, 1.0).
severity_weight(malaria, headache, 1.0).
severity_weight(malaria, nausea, 1.0).
severity_weight(malaria, vomiting, 1.0).
severity_weight(malaria, body_ache, 1.0).
severity_weight(dengue, fever, 1.0).
severity_weight(dengue, headache, 1.0).
severity_weight(dengue, joint_pain, 1.2).
severity_weight(dengue, muscle_pain, 1.0).
severity_weight(dengue, rash, 1.2).
severity_weight(dengue, nausea, 1.0).
severity_weight(dengue, vomiting, 1.0).
severity_weight(dengue, swollen_glands, 1.0).
severity_weight(typhoid, fever, 1.0).
severity_weight(typhoid, headache, 1.0).
severity_weight(typhoid, fatigue, 1.0).
severity_weight(typhoid, nausea, 1.0).
severity_weight(typhoid, vomiting, 1.0).
severity_weight(typhoid, diarrhea, 1.0).
severity_weight(typhoid, loss_of_appetite, 1.0).
severity_weight(typhoid, abdominal_pain, 1.0).
severity_weight(migraine, headache, 1.0).
severity_weight(migraine, nausea, 1.0).
severity_weight(migraine, vomiting, 1.0).
severity_weight(migraine, blurred_vision, 1.0).
severity_weight(migraine, dizziness, 1.0).
severity_weight(migraine, sensitivity_to_light, 1.3).
severity_weight(asthma, shortness_of_breath, 1.0).
severity_weight(asthma, wheezing, 1.0).
severity_weight(asthma, chest_pain, 1.0).
severity_weight(asthma, cough, 1.0).
severity_weight(asthma, fatigue, 1.0).
severity_weight(pneumonia, fever, 1.0).
severity_weight(pneumonia, cough, 1.0).
severity_weight(pneumonia, shortness_of_breath, 1.4).
severity_weight(pneumonia, chest_pain, 1.3).
severity_weight(pneumonia, fatigue, 1.0).
severity_weight(pneumonia, chills, 1.0).
severity_weight(pneumonia, sweating, 1.0).
severity_weight(pneumonia, nausea, 1.0).
severity_weight(diabetes, frequent_urination, 1.3).
severity_weight(diabetes, increased_thirst, 1.3).
severity_weight(diabetes, fatigue, 1.0).
severity_weight(diabetes, blurred_vision, 1.0).
severity_weight(diabetes, weight_loss, 1.0).
severity_weight(hypertension, headache, 1.0).
severity_weight(hypertension, dizziness, 1.0).
severity_weight(hypertension, chest_pain, 1.0).
severity_weight(hypertension, shortness_of_breath, 1.0).
severity_weight(hypertension, blurred_vision, 1.0).
severity_weight(anemia, fatigue, 1.0).
severity_weight(anemia, pale_skin, 1.0).
severity_weight(anemia, dizziness, 1.0).
severity_weight(anemia, shortness_of_breath, 1.0).
severity_weight(anemia, cold_hands_and_feet, 1.0).
severity_weight(anemia, headache, 1.0).
severity_weight(allergy, sneezing, 1.0).
severity_weight(allergy, itchy_eyes, 1.0).
severity_weight(allergy, runny_nose, 1.0).
severity_weight(allergy, rash, 1.0).
severity_weight(allergy, cough, 1.0).
severity_weight(allergy, nasal_congestion, 1.0).
severity_weight(chickenpox, fever, 1.0).
severity_weight(chickenpox, rash, 1.0).
severity_weight(chickenpox, fatigue, 1.0).
severity_weight(chickenpox, headache, 1.0).
severity_weight(chickenpox, loss_of_appetite, 1.0).
severity_weight(measles, fever, 1.0).
severity_weight(measles, rash, 1.0).
severity_weight(measles, cough, 1.0).
severity_weight(measles, runny_nose, 1.0).
severity_weight(measles, red_eyes, 1.0).
severity_weight(measles, fatigue, 1.0).
severity_weight(hepatitis_a, fever, 1.0).
severity_weight(hepatitis_a, fatigue, 1.0).
severity_weight(hepatitis_a, nausea, 1.0).
severity_weight(hepatitis_a, vomiting, 1.0).
severity_weight(hepatitis_a, abdominal_pain, 1.0).
severity_weight(hepatitis_a, yellowing_of_skin, 1.5).
severity_weight(hepatitis_a, loss_of_appetite, 1.0).
severity_weight(tuberculosis, cough, 1.0).
severity_weight(tuberculosis, fever, 1.0).
severity_weight(tuberculosis, night_sweats, 1.3).
severity_weight(tuberculosis, weight_loss, 1.0).
severity_weight(tuberculosis, fatigue, 1.0).
severity_weight(tuberculosis, chest_pain, 1.0).
severity_weight(tuberculosis, coughing_blood, 1.5).
severity_weight(bronchitis, cough, 1.0).
severity_weight(bronchitis, fatigue, 1.0).
severity_weight(bronchitis, chest_pain, 1.0).
severity_weight(bronchitis, shortness_of_breath, 1.0).
severity_weight(bronchitis, wheezing, 1.0).
severity_weight(bronchitis, fever, 1.0).
severity_weight(sinusitis, facial_pain, 1.0).
severity_weight(sinusitis, nasal_congestion, 1.0).
severity_weight(sinusitis, headache, 1.0).
severity_weight(sinusitis, runny_nose, 1.0).
severity_weight(sinusitis, fatigue, 1.0).
severity_weight(sinusitis, fever, 1.0).
severity_weight(urinary_tract_infection, burning_urination, 1.4).
severity_weight(urinary_tract_infection, frequent_urination, 1.0).
severity_weight(urinary_tract_infection, abdominal_pain, 1.0).
severity_weight(urinary_tract_infection, blood_in_urine, 1.3).
severity_weight(urinary_tract_infection, fever, 1.0).
severity_weight(gastroenteritis, diarrhea, 1.0).
severity_weight(gastroenteritis, vomiting, 1.0).
severity_weight(gastroenteritis, nausea, 1.0).
severity_weight(gastroenteritis, abdominal_pain, 1.0).
severity_weight(gastroenteritis, fever, 1.0).
severity_weight(gastroenteritis, bloating, 1.0).
severity_weight(heat_stroke, fever, 1.0).
severity_weight(heat_stroke, headache, 1.0).
severity_weight(heat_stroke, dizziness, 1.0).
severity_weight(heat_stroke, nausea, 1.0).
severity_weight(heat_stroke, confusion, 1.5).
severity_weight(heat_stroke, rapid_heartbeat, 1.3).
severity_weight(insomnia, insomnia, 1.0).
severity_weight(insomnia, fatigue, 1.0).
severity_weight(insomnia, headache, 1.0).
severity_weight(insomnia, difficulty_concentrating, 1.0).
severity_weight(insomnia, dizziness, 1.0).
severity_weight(depression, sadness, 1.0).
severity_weight(depression, loss_of_interest, 1.0).
severity_weight(depression, fatigue, 1.0).
severity_weight(depression, insomnia, 1.0).
severity_weight(depression, difficulty_concentrating, 1.0).
severity_weight(depression, loss_of_appetite, 1.0).
severity_weight(arthritis, joint_pain, 1.0).
severity_weight(arthritis, stiff_joints, 1.0).
severity_weight(arthritis, fatigue, 1.0).
severity_weight(arthritis, back_pain, 1.0).
severity_weight(arthritis, muscle_pain, 1.0).

% Age-based risk factors
risk_factor(flu, age, child).
risk_factor(flu, age, elderly).
risk_factor(covid19, age, elderly).
risk_factor(pneumonia, age, child).
risk_factor(pneumonia, age, elderly).
risk_factor(diabetes, age, middle_aged).
risk_factor(diabetes, age, elderly).
risk_factor(hypertension, age, middle_aged).
risk_factor(hypertension, age, elderly).
risk_factor(arthritis, age, elderly).

% ------------------- GENERATED FACTS (END) -------------------

% ------------------- Severity Scaling (user-reported severity) -------------------
% The GUI lets the patient rate each reported symptom Mild/Moderate/Severe.
% These factors scale that symptom's contribution to the confidence score.
severity_factor(mild, 0.8).
severity_factor(moderate, 1.0).
severity_factor(severe, 1.25).

% ------------------- Counts over Dynamic Patient Facts -------------------
% The controller asserts patient_has(Symptom) and patient_sev(Symptom, Severity)
% before running a diagnosis.

total_symptoms(Disease, Count) :-
    findall(S, has_symptom(Disease, S), Symptoms),
    length(Symptoms, Count).

matched_symptoms(Disease, Count) :-
    findall(S, (has_symptom(Disease, S), patient_has(S)), Matched),
    length(Matched, Count).

possible_disease(Disease) :-
    disease(Disease),
    matched_symptoms(Disease, Count),
    Count >= 2.

% ------------------- Confidence Calculation -------------------
% Confidence is the patient's severity-weighted symptom score divided by the
% disease's total (equally defaulted) weight, so the result can never exceed
% 100%, even when every symptom is reported as severe.

total_weight(Disease, Denominator) :-
    findall(Weight,
            (has_symptom(Disease, Symptom), severity_weight(Disease, Symptom, Weight)),
            Weights),
    sum_list(Weights, Denominator).

matched_weight(Disease, Numerator) :-
    findall(Weight,
            (has_symptom(Disease, Symptom),
             patient_has(Symptom),
             severity_weight(Disease, Symptom, Base),
             (patient_sev(Symptom, Severity) -> severity_factor(Severity, Factor) ; Factor = 1.0),
             Weight is Base * Factor),
            Weights),
    sum_list(Weights, Numerator).

confidence(Disease, Percentage) :-
    matched_weight(Disease, Numerator),
    total_weight(Disease, Denominator),
    Denominator > 0,
    Raw is round((Numerator / Denominator) * 100),
    (Raw > 100 -> Percentage = 100 ; Percentage = Raw).

% ------------------- Knowledge Base Accessors -------------------
get_disease_symptoms(Disease, Symptoms) :-
    findall(Symptom, has_symptom(Disease, Symptom), Symptoms).

get_all_diseases(Diseases) :-
    findall(Disease, disease(Disease), Diseases).

get_all_symptoms(Symptoms) :-
    findall(Symptom, symptom(Symptom), Symptoms).
