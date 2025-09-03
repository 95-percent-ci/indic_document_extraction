writing_system_to_language = {'Devanagari': ['hindi','sanskrit','nepali','konkani', 'maithali', 'marathi'],
                              'tamil': ['tamil'],'telugu': ['telugu'],'Kannada': ['kannada'],'Malayalam': ['malayalam'],
                              'Bengali': ['bengali', 'assamese'],'Meetei-mayek': ['manipuri'],'Gujarati': ['gujarati'],
                              'Gurmukhi': ['punjabi'],'Odia': ['oriya'],'Arabic': ['kashmiri', 'sindhi', 'urdu'],
                              'Latin': ['english'],'Ol-chiki': ['santali']}


language_to_writing_system = {
    "marathi": ["Devanagari"], "hindi": ["Devanagari"], "sanskrit": ["Devanagari"],
    "tamil": ["tamil"], "telugu": ["telugu"], "kannada": ["Kannada"],"malayalam": ["Malayalam"],
    "bengali": ["Bengali"], "assamese": ["Bengali"],"manipuri": ["Meetei-mayek"],"nepali": ["Devanagari"],
    "gujarati": ["Gujarati"], "punjabi": ["Gurmukhi"], "konkani": ["Devanagari"],"oriya": ["Odia"],"kashmiri": ["Arabic"], 
    "sindhi": ["Arabic", "Devanagari"], "urdu": ["Arabic"],"english": ["Latin"], "santali": ["Ol-chiki"],
    "maithali": ["Devanagari"], "dogri": ["Devanagari"], "bodo": ["Devanagari"]
    }

## code map for normalisation
language_code_norm_map = {"sanskrit": "sa", "hindi": "hi", "konkani": "kK","punjabi": "pa", "nepali" :"ne", "sindhi": "sd", "bengali": "bn", 
                     "assamese": "as", "gujarati": "gu", "marathi": "mr", "odia": "or", "kannada": "kn", "malayalam": "ml", 
                     "telugu": "te", "tamil": "ta"}