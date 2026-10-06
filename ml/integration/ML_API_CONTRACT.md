\# SmartMed ML API Contract



\## 1. Purpose



This document defines the interface between the SmartMed backend and the ML + Disposal Intelligence module.



The ML module performs:



1\. Drug-class classification using medicine information.

2\. Confidence scoring and top-3 predictions.

3\. Expiry-status checking using the expiry date provided for the medicine package.

4\. Rule-based disposal guidance.



The ML model does \*\*not\*\* predict whether a medicine is expired.



The actual expiry date is package/batch-specific and must be supplied by the user or backend.



\---



\## 2. Intelligence Flow



```text

Frontend

&#x20;  |

&#x20;  | Medicine information + package expiry date

&#x20;  v

Backend

&#x20;  |

&#x20;  | ML input

&#x20;  v

SmartMed ML Module

&#x20;  |

&#x20;  +--> Drug-class classification

&#x20;  |

&#x20;  +--> Confidence + top-3 predictions

&#x20;  |

&#x20;  +--> Disposal Guidance Engine

&#x20;  |

&#x20;  v

Backend

&#x20;  |

&#x20;  | ML response

&#x20;  v

Frontend





3\. ML Input

The backend should provide the following fields.

Field	Type	Required	Example

generic	string	Yes	Paracetamol

dosage\_form	string	Yes	Tablet

type	string	Yes	allopathic

strength	string	Yes	500 mg

expiry\_date	string/null	Yes	2026-08-01





Example request

{

&#x20; "generic": "Paracetamol",

&#x20; "dosage\_form": "Tablet",

&#x20; "type": "allopathic",

&#x20; "strength": "500 mg",

&#x20; "expiry\_date": "2026-08-01"

}



4\. ML Model Features

The drug-class classification model uses these four medicine features:

generic

dosage form

type

strength



The expiry\_date is NOT used as a machine-learning feature.

It is used separately by the disposal guidance engine.

5\. Model

Algorithm

The current model uses:

TF-IDF

\+

One-Hot Encoding

\+

Logistic Regression



Training data

The training dataset contains:

20,276 records

235 drug classes



The dataset was created by joining medicine information with generic-medicine information.

Drug classes with fewer than 10 records were excluded from the training dataset to reduce extremely small classes.

6\. Model Evaluation

The current test split contains:

Training samples: 16,220

Testing samples:   4,056



Evaluation results:

Metric	Score

Accuracy	96.84%

Macro Precision	96.04%

Macro Recall	91.02%

Macro F1	92.69%





The model should be described as:

A drug-class classification model achieving 96.84% test accuracy and 0.9269 macro F1 across 235 drug classes.



Do not describe the model as having 96.84% accuracy for every individual medicine.

7\. Model File

The trained model is stored at:

ml/model/drug\_class\_classifier.joblib



The backend/integration layer should load this model rather than retraining it during normal API requests.

8\. ML Output

The ML module returns:

{

&#x20; "predicted\_drug\_class": "Non opioid analgesics",

&#x20; "confidence": 0.9690,

&#x20; "top\_predictions": \[

&#x20;   {

&#x20;     "drug\_class": "Non opioid analgesics",

&#x20;     "confidence": 0.9690

&#x20;   },

&#x20;   {

&#x20;     "drug\_class": "Drugs for Osteoarthritis",

&#x20;     "confidence": 0.0016

&#x20;   },

&#x20;   {

&#x20;     "drug\_class": "Amoebicides",

&#x20;     "confidence": 0.0014

&#x20;   }

&#x20; ],

&#x20; "disposal\_guidance": {

&#x20;   "expiry\_status": "EXPIRED",

&#x20;   "handling\_category": "PHARMACEUTICAL\_WASTE",

&#x20;   "recommended\_route": "RETURN\_TO\_MANUFACTURER\_OR\_AUTHORIZED\_INCINERATION",

&#x20;   "warning": "Use an authorized pharmaceutical-waste route. Do not dispose of the medicine by household destruction."

&#x20; }

}



9\. Top Predictions

The model returns the three highest-probability drug-class predictions.

Each prediction contains:

{

&#x20; "drug\_class": "Non opioid analgesics",

&#x20; "confidence": 0.9690

}



The confidence value is returned as a decimal between 0 and 1.

For example:

0.9690 = 96.90%



10\. Disposal Guidance

Disposal guidance is handled separately from machine learning.

The model predicts the drug class.

The disposal engine then uses:

Predicted drug class

\+

Package expiry date



to determine the appropriate application-level guidance.

Therefore:

ML prediction != disposal decision



The ML model supports the disposal engine by identifying the drug class.

11\. Expiry Status

The disposal engine supports four expiry states.

A. EXPIRY\_UNKNOWN

Used when no expiry date is provided.

Example:

{

&#x20; "expiry\_status": "EXPIRY\_UNKNOWN",

&#x20; "handling\_category": "EXPIRY\_VERIFICATION\_REQUIRED",

&#x20; "recommended\_route": "VERIFY\_PACKAGE\_EXPIRY\_DATE"

}



The user must verify the actual expiry date printed on the medicine package.

B. INVALID\_EXPIRY\_DATE

Used when the provided expiry date cannot be parsed.

Example:

{

&#x20; "expiry\_status": "INVALID\_EXPIRY\_DATE",

&#x20; "handling\_category": "EXPIRY\_VERIFICATION\_REQUIRED",

&#x20; "recommended\_route": "VERIFY\_PACKAGE\_EXPIRY\_DATE"

}



C. NOT\_EXPIRED

Used when the supplied package expiry date has not passed.

Example:

{

&#x20; "expiry\_status": "NOT\_EXPIRED",

&#x20; "handling\_category": "NOT\_EXPIRED",

&#x20; "recommended\_route": "NO\_EXPIRED\_MEDICINE\_DISPOSAL\_REQUIRED"

}



D. EXPIRED

Used when the supplied package expiry date has passed.

The disposal engine then determines the appropriate handling category based on the predicted drug class.

12\. Current Disposal Categories

The current implementation supports:

PHARMACEUTICAL\_WASTE

CYTOTOXIC\_PHARMACEUTICAL\_WASTE

NOT\_EXPIRED

EXPIRY\_VERIFICATION\_REQUIRED



The project should use authorized pharmaceutical-waste collection/treatment routes.

The system should not instruct users to destroy medicines themselves at home.

13\. Cytotoxic Handling

The current rule-based engine explicitly recognizes these drug classes:

Cytotoxic Chemotherapy

Cytotoxic immunosuppressants

Hormonal Chemotherapy

Immunological Chemotherapy



These are handled as:

CYTOTOXIC\_PHARMACEUTICAL\_WASTE



Other drug classes should not automatically be labelled cytotoxic unless the project adds an authoritative rule for them.

14\. Python Integration Function

The current integration module provides:

analyze\_medicine(    generic,    dosage\_form,    medicine\_type,    strength,    expiry\_date,)





Example:

result = analyze\_medicine(    generic="Paracetamol",    dosage\_form="Tablet",    medicine\_type="allopathic",    strength="500 mg",    expiry\_date="2026-08-01",)





The function returns the complete ML + disposal result.

15\. Existing Integration File

The main integration implementation is:

ml/integration/smartmed\_intelligence.py



The disposal rules are implemented in:

ml/disposal/disposal\_engine.py



The prediction helper is:

ml/prediction/predict.py



The trained model is:

ml/model/drug\_class\_classifier.joblib



16\. Backend Integration Recommendation

The backend should call the ML integration layer after collecting the required medicine information.

Recommended flow:

1\. User selects/searches medicine

2\. Backend obtains medicine information

3\. User provides package expiry date

4\. Backend sends ML input

5\. ML predicts drug class

6\. Disposal engine checks expiry status

7\. Disposal engine generates guidance

8\. Backend returns the result to frontend

9\. Frontend displays drug class + disposal guidance



17\. Example Backend Request

{

&#x20; "generic": "Paracetamol",

&#x20; "dosage\_form": "Tablet",

&#x20; "type": "allopathic",

&#x20; "strength": "500 mg",

&#x20; "expiry\_date": "2026-08-01"

}



18\. Example Backend Response

{

&#x20; "predicted\_drug\_class": "Non opioid analgesics",

&#x20; "confidence": 0.9690,

&#x20; "top\_predictions": \[

&#x20;   {

&#x20;     "drug\_class": "Non opioid analgesics",

&#x20;     "confidence": 0.9690

&#x20;   },

&#x20;   {

&#x20;     "drug\_class": "Drugs for Osteoarthritis",

&#x20;     "confidence": 0.0016

&#x20;   },

&#x20;   {

&#x20;     "drug\_class": "Amoebicides",

&#x20;     "confidence": 0.0014

&#x20;   }

&#x20; ],

&#x20; "disposal\_guidance": {

&#x20;   "expiry\_status": "EXPIRED",

&#x20;   "handling\_category": "PHARMACEUTICAL\_WASTE",

&#x20;   "recommended\_route": "RETURN\_TO\_MANUFACTURER\_OR\_AUTHORIZED\_INCINERATION",

&#x20;   "warning": "Use an authorized pharmaceutical-waste route. Do not dispose of the medicine by household destruction."

&#x20; }

}



19\. Important Integration Notes

Do not send these fields to the model:

medicine\_id

user\_id

tracking\_id

quantity

collection\_point

request\_status



These belong to the application/backend layer.

ML requires only:

generic

dosage\_form

type

strength

expiry\_date



Of these, only the first four are model features.

20\. Important Expiry Rule

The medicine dataset contains medicine information but does not provide the actual batch/package expiry date for a user's medicine.

Therefore:

Medicine name != expiry date



The backend/frontend must obtain the actual expiry date from the medicine package or user input.

The ML model must not be used to predict expiry.

21\. Files for Member 1

Member 1 needs these files/modules:

ml/model/drug\_class\_classifier.joblib

ml/integration/smartmed\_intelligence.py

ml/disposal/disposal\_engine.py

ml/prediction/predict.py



And this contract:

ml/integration/ML\_API\_CONTRACT.md



22\. Current Status

ML + Analytics + Disposal Intelligence:

Dataset analysis              COMPLETE

Data preprocessing             COMPLETE

Training dataset               COMPLETE

Drug-class ML model            COMPLETE

Model evaluation               COMPLETE

Evaluation graphs              COMPLETE

Prediction module              COMPLETE

Disposal guidance engine       COMPLETE

ML integration module          COMPLETE

Backend handoff contract       COMPLETE

