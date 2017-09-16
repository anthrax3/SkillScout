import nltk

# industries as reference (we have so)
lIndustries = [ "Agriculture, Forestry, Fishing",
 "Mining",
  "Manufacturing",
   "Electricity, Gas, Water, Waste Services",
    "Construction",
     "Wholesale Trade",
      "Retail Trade",
       "Accommodation and Food Services",
        "Transport, Postal and Warehousing",
         "Information Media and Telecommunications",
          "Financial and Insurance Services",
           "Rental, Hiring and Real Estate Services",
            "Professional, Scientific, Technical Services",
             "Administrative and Support Services",
              "Public Administration and Safety",
               "Education and Training",
                "Health Care and Social Assistance",
                 "Arts and Recreation Services"]

lTrainingData = [(),(),(),(),(),()]
classifier = nltk.NaiveBayesClassifier.train(lTrainingData)
