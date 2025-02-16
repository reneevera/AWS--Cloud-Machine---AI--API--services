aws comprehend detect-entities --language-code en --text "Renee Vera jvera3@my.centennialcollege.ca (416) 222 3441 233 Hoey crescent M3E1R7 Toronto Ontario Centennial college" > renee_comprehend_output.json


aws comprehendmedical detect-phi --text "Renee Vera jvera3@my.centennialcollege.ca (416) 222 3441 233 Hoey crescent M3E1R7 Toronto Ontario Centennial college" > renee_comprehend_medical_output.json