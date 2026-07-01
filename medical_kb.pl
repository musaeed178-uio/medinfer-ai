% ============================================================
% Medical Expert System - Enhanced Knowledge Base (Prolog)
% ============================================================

% ------------------- Diseases -------------------
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

% ------------------- Disease Categories -------------------
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

% ------------------- Disease Descriptions -------------------
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

% ------------------- Recommendations -------------------
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

% ------------------- Emergency Flags -------------------
is_emergency(covid19).
is_emergency(malaria).
is_emergency(dengue).
is_emergency(pneumonia).
is_emergency(tuberculosis).
is_emergency(heat_stroke).
is_emergency(hepatitis_a).

% ------------------- Symptoms -------------------
symptom(fever).
symptom(cough).
symptom(headache).
symptom(fatigue).
symptom(body_ache).
symptom(sore_throat).
symptom(runny_nose).
symptom(shortness_of_breath).
symptom(chills).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(rash).
symptom(joint_pain).
symptom(muscle_pain).
symptom(loss_of_appetite).
symptom(sweating).
symptom(dizziness).
symptom(chest_pain).
symptom(wheezing).
symptom(blurred_vision).
symptom(frequent_urination).
symptom(weight_loss).
symptom(increased_thirst).
symptom(pale_skin).
symptom(cold_hands_and_feet).
symptom(sneezing).
symptom(itchy_eyes).
symptom(swollen_glands).
symptom(back_pain).
symptom(insomnia).
symptom(sensitivity_to_light).
symptom(red_eyes).
symptom(abdominal_pain).
symptom(yellowing_of_skin).
symptom(blood_in_urine).
symptom(burning_urination).
symptom(bloating).
symptom(confusion).
symptom(rapid_heartbeat).
symptom(stiff_neck).
symptom(night_sweats).
symptom(coughing_blood).
symptom(facial_pain).
symptom(nasal_congestion).
symptom(sadness).
symptom(loss_of_interest).
symptom(difficulty_concentrating).
symptom(stiff_joints).
symptom(skin_rash).

% ------------------- Disease-Symptom Facts -------------------
% Flu
has_symptom(flu, fever).
has_symptom(flu, cough).
has_symptom(flu, headache).
has_symptom(flu, fatigue).
has_symptom(flu, body_ache).
has_symptom(flu, chills).
has_symptom(flu, sore_throat).

% Cold
has_symptom(cold, runny_nose).
has_symptom(cold, sneezing).
has_symptom(cold, sore_throat).
has_symptom(cold, cough).
has_symptom(cold, headache).
has_symptom(cold, fatigue).
has_symptom(cold, nasal_congestion).

% COVID-19
has_symptom(covid19, fever).
has_symptom(covid19, cough).
has_symptom(covid19, shortness_of_breath).
has_symptom(covid19, fatigue).
has_symptom(covid19, body_ache).
has_symptom(covid19, headache).
has_symptom(covid19, loss_of_appetite).
has_symptom(covid19, sore_throat).

% Malaria
has_symptom(malaria, fever).
has_symptom(malaria, chills).
has_symptom(malaria, sweating).
has_symptom(malaria, headache).
has_symptom(malaria, nausea).
has_symptom(malaria, vomiting).
has_symptom(malaria, body_ache).

% Dengue
has_symptom(dengue, fever).
has_symptom(dengue, headache).
has_symptom(dengue, joint_pain).
has_symptom(dengue, muscle_pain).
has_symptom(dengue, rash).
has_symptom(dengue, nausea).
has_symptom(dengue, vomiting).
has_symptom(dengue, swollen_glands).

% Typhoid
has_symptom(typhoid, fever).
has_symptom(typhoid, headache).
has_symptom(typhoid, fatigue).
has_symptom(typhoid, nausea).
has_symptom(typhoid, vomiting).
has_symptom(typhoid, diarrhea).
has_symptom(typhoid, loss_of_appetite).
has_symptom(typhoid, abdominal_pain).

% Migraine
has_symptom(migraine, headache).
has_symptom(migraine, nausea).
has_symptom(migraine, vomiting).
has_symptom(migraine, blurred_vision).
has_symptom(migraine, dizziness).
has_symptom(migraine, sensitivity_to_light).

% Asthma
has_symptom(asthma, shortness_of_breath).
has_symptom(asthma, wheezing).
has_symptom(asthma, chest_pain).
has_symptom(asthma, cough).
has_symptom(asthma, fatigue).

% Pneumonia
has_symptom(pneumonia, fever).
has_symptom(pneumonia, cough).
has_symptom(pneumonia, shortness_of_breath).
has_symptom(pneumonia, chest_pain).
has_symptom(pneumonia, fatigue).
has_symptom(pneumonia, chills).
has_symptom(pneumonia, sweating).
has_symptom(pneumonia, nausea).

% Diabetes
has_symptom(diabetes, frequent_urination).
has_symptom(diabetes, increased_thirst).
has_symptom(diabetes, fatigue).
has_symptom(diabetes, blurred_vision).
has_symptom(diabetes, weight_loss).

% Hypertension
has_symptom(hypertension, headache).
has_symptom(hypertension, dizziness).
has_symptom(hypertension, chest_pain).
has_symptom(hypertension, shortness_of_breath).
has_symptom(hypertension, blurred_vision).

% Anemia
has_symptom(anemia, fatigue).
has_symptom(anemia, pale_skin).
has_symptom(anemia, dizziness).
has_symptom(anemia, shortness_of_breath).
has_symptom(anemia, cold_hands_and_feet).
has_symptom(anemia, headache).

% Allergy
has_symptom(allergy, sneezing).
has_symptom(allergy, itchy_eyes).
has_symptom(allergy, runny_nose).
has_symptom(allergy, rash).
has_symptom(allergy, cough).
has_symptom(allergy, nasal_congestion).

% Chickenpox
has_symptom(chickenpox, fever).
has_symptom(chickenpox, rash).
has_symptom(chickenpox, fatigue).
has_symptom(chickenpox, headache).
has_symptom(chickenpox, loss_of_appetite).

% Measles
has_symptom(measles, fever).
has_symptom(measles, rash).
has_symptom(measles, cough).
has_symptom(measles, runny_nose).
has_symptom(measles, red_eyes).
has_symptom(measles, fatigue).

% Hepatitis A
has_symptom(hepatitis_a, fever).
has_symptom(hepatitis_a, fatigue).
has_symptom(hepatitis_a, nausea).
has_symptom(hepatitis_a, vomiting).
has_symptom(hepatitis_a, abdominal_pain).
has_symptom(hepatitis_a, yellowing_of_skin).
has_symptom(hepatitis_a, loss_of_appetite).

% Tuberculosis
has_symptom(tuberculosis, cough).
has_symptom(tuberculosis, fever).
has_symptom(tuberculosis, night_sweats).
has_symptom(tuberculosis, weight_loss).
has_symptom(tuberculosis, fatigue).
has_symptom(tuberculosis, chest_pain).
has_symptom(tuberculosis, coughing_blood).

% Bronchitis
has_symptom(bronchitis, cough).
has_symptom(bronchitis, fatigue).
has_symptom(bronchitis, chest_pain).
has_symptom(bronchitis, shortness_of_breath).
has_symptom(bronchitis, wheezing).
has_symptom(bronchitis, fever).

% Sinusitis
has_symptom(sinusitis, facial_pain).
has_symptom(sinusitis, nasal_congestion).
has_symptom(sinusitis, headache).
has_symptom(sinusitis, runny_nose).
has_symptom(sinusitis, fatigue).
has_symptom(sinusitis, fever).

% Urinary Tract Infection
has_symptom(urinary_tract_infection, burning_urination).
has_symptom(urinary_tract_infection, frequent_urination).
has_symptom(urinary_tract_infection, abdominal_pain).
has_symptom(urinary_tract_infection, blood_in_urine).
has_symptom(urinary_tract_infection, fever).

% Gastroenteritis
has_symptom(gastroenteritis, diarrhea).
has_symptom(gastroenteritis, vomiting).
has_symptom(gastroenteritis, nausea).
has_symptom(gastroenteritis, abdominal_pain).
has_symptom(gastroenteritis, fever).
has_symptom(gastroenteritis, bloating).

% Heat Stroke
has_symptom(heat_stroke, fever).
has_symptom(heat_stroke, headache).
has_symptom(heat_stroke, dizziness).
has_symptom(heat_stroke, nausea).
has_symptom(heat_stroke, confusion).
has_symptom(heat_stroke, rapid_heartbeat).

% Insomnia
has_symptom(insomnia, insomnia).
has_symptom(insomnia, fatigue).
has_symptom(insomnia, headache).
has_symptom(insomnia, difficulty_concentrating).
has_symptom(insomnia, dizziness).

% Depression
has_symptom(depression, sadness).
has_symptom(depression, loss_of_interest).
has_symptom(depression, fatigue).
has_symptom(depression, insomnia).
has_symptom(depression, difficulty_concentrating).
has_symptom(depression, loss_of_appetite).

% Arthritis
has_symptom(arthritis, joint_pain).
has_symptom(arthritis, stiff_joints).
has_symptom(arthritis, fatigue).
has_symptom(arthritis, back_pain).
has_symptom(arthritis, muscle_pain).

% ------------------- Severity Weights -------------------
% Some symptoms are more indicative of certain diseases
severity_weight(flu, fever, 1.2).
severity_weight(flu, body_ache, 1.1).
severity_weight(covid19, shortness_of_breath, 1.5).
severity_weight(covid19, loss_of_appetite, 1.1).
severity_weight(malaria, chills, 1.3).
severity_weight(dengue, rash, 1.2).
severity_weight(dengue, joint_pain, 1.2).
severity_weight(pneumonia, shortness_of_breath, 1.4).
severity_weight(pneumonia, chest_pain, 1.3).
severity_weight(tuberculosis, coughing_blood, 1.5).
severity_weight(tuberculosis, night_sweats, 1.3).
severity_weight(hepatitis_a, yellowing_of_skin, 1.5).
severity_weight(diabetes, frequent_urination, 1.3).
severity_weight(diabetes, increased_thirst, 1.3).
severity_weight(migraine, sensitivity_to_light, 1.3).
severity_weight(heat_stroke, confusion, 1.5).
severity_weight(heat_stroke, rapid_heartbeat, 1.3).
severity_weight(urinary_tract_infection, burning_urination, 1.4).
severity_weight(urinary_tract_infection, blood_in_urine, 1.3).

% Default severity weight
severity_weight(_, _, 1.0).

% ------------------- Risk Factors -------------------
% Age-based risk factors
risk_factor(flu, age, child).
risk_factor(flu, age, elderly).
risk_factor(covid19, age, elderly).
risk_factor(pneumonia, age, child).
risk_factor(pneumonia, age, elderly).
risk_factor(hypertension, age, middle_aged).
risk_factor(hypertension, age, elderly).
risk_factor(diabetes, age, middle_aged).
risk_factor(diabetes, age, elderly).
risk_factor(arthritis, age, elderly).
risk_factor(alzheimer, age, elderly).

% ------------------- Confidence Calculation -------------------
total_symptoms(Disease, Count) :-
    findall(S, has_symptom(Disease, S), Symptoms),
    length(Symptoms, Count).

matched_symptoms(Disease, PatientSymptoms, Count) :-
    findall(S, (has_symptom(Disease, S), member(S, PatientSymptoms)), Matched),
    length(Matched, Count).

% Weighted confidence calculation
weighted_confidence(Disease, PatientSymptoms, Percentage) :-
    findall(
        Weight,
        (has_symptom(Disease, S), member(S, PatientSymptoms), severity_weight(Disease, S, Weight)),
        Weights
    ),
    sum_list(Weights, WeightedSum),
    total_symptoms(Disease, Total),
    Total > 0,
    Percentage is round((WeightedSum / Total) * 100).

confidence(Disease, PatientSymptoms, Percentage) :-
    weighted_confidence(Disease, PatientSymptoms, Percentage).

% ------------------- Diagnosis Rules -------------------
possible_disease(Disease, PatientSymptoms) :-
    disease(Disease),
    matched_symptoms(Disease, PatientSymptoms, Count),
    Count >= 2.

diagnosis(PatientSymptoms, Results) :-
    findall(
        (Disease, Conf, Matched, Total),
        (
            possible_disease(Disease, PatientSymptoms),
            confidence(Disease, PatientSymptoms, Conf),
            matched_symptoms(Disease, PatientSymptoms, Matched),
            total_symptoms(Disease, Total)
        ),
        RawResults
    ),
    sort_by_confidence(RawResults, Results).

sort_by_confidence(RawResults, Sorted) :-
    map_list_to_pairs(get_confidence, RawResults, Pairs),
    keysort(Pairs, SortedPairs),
    reverse(SortedPairs, RevSorted),
    pairs_values(RevSorted, Sorted).

get_confidence((_, Conf, _, _), Conf).

% ------------------- Explanation Rules -------------------
explain_diagnosis(Disease, PatientSymptoms, Explanation) :-
    findall(S, (has_symptom(Disease, S), member(S, PatientSymptoms)), Matched),
    findall(S, (has_symptom(Disease, S), \+ member(S, PatientSymptoms)), Missing),
    confidence(Disease, PatientSymptoms, Conf),
    format_message(Disease, Conf, Matched, Missing, Explanation).

format_message(Disease, Conf, Matched, Missing, Explanation) :-
    atomic_list_concat(Matched, ', ', MatchedStr),
    atomic_list_concat(Missing, ', ', MissingStr),
    format(string(Explanation),
           'Possible Diagnosis: ~w~nConfidence: ~w%~nMatched Symptoms: ~w~nMissing Symptoms: ~w',
           [Disease, Conf, MatchedStr, MissingStr]).

% ------------------- Forward Chaining -------------------
forward_chain(PatientSymptoms, Conclusions) :-
    findall(
        (Disease, Conf),
        (
            disease(Disease),
            matched_symptoms(Disease, PatientSymptoms, Count),
            Count >= 2,
            confidence(Disease, PatientSymptoms, Conf),
            Conf >= 30
        ),
        Conclusions
    ).

% ------------------- Backward Chaining -------------------
verify_disease(Disease, PatientSymptoms) :-
    disease(Disease),
    findall(S, has_symptom(Disease, S), RequiredSymptoms),
    verify_symptoms(RequiredSymptoms, PatientSymptoms, Verified),
    length(RequiredSymptoms, Total),
    length(Verified, Matched),
    Matched >= 2,
    Matched =< Total.

verify_symptoms([], _, []).
verify_symptoms([S|Rest], PatientSymptoms, [S|Verified]) :-
    member(S, PatientSymptoms),
    verify_symptoms(Rest, PatientSymptoms, Verified).
verify_symptoms([_|Rest], PatientSymptoms, Verified) :-
    verify_symptoms(Rest, PatientSymptoms, Verified).

% ------------------- Disease by Category -------------------
diseases_by_category(Category, Diseases) :-
    findall(D, (disease(D), category(D, Category)), Diseases).

all_categories(Categories) :-
    findall(C, category(_, C), Raw),
    sort(Raw, Categories).

% ------------------- Get Disease Info -------------------
get_disease_info(Disease, Info) :-
    disease(Disease),
    description(Disease, Desc),
    category(Disease, Cat),
    recommendation(Disease, Rec),
    (is_emergency(Disease) -> Emerg = true ; Emerg = false),
    Info = (Disease, Desc, Cat, Rec, Emerg).

% ------------------- Utility Predicates -------------------
get_disease_symptoms(Disease, Symptoms) :-
    findall(S, has_symptom(Disease, S), Symptoms).

get_all_diseases(Diseases) :-
    findall(D, disease(D), Diseases).

get_all_symptoms(Symptoms) :-
    findall(S, symptom(S), Symptoms).

cleanup :-
    retractall(patient_has(_)).
