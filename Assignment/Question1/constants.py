PRELOADED_MEDICINES = [
    # Pain Relief
    ("PR4560", "Panadol", "12 pcs", 5.90, 120),
    ("PR6678", "Panadol Extra", "12 pcs", 7.50, 80),
    ("PR1694", "Panadol Actifast", "20 pcs", 13.90, 60),
    ("PR5611", "Uphamol 500mg", "20 pcs", 6.50, 90),
    ("PR1364", "Nurofen 200mg", "24 pcs", 18.90, 50),
    ("PR9977", "Disprin", "10 pcs", 6.20, 40),
    ("PR6588", "Voltaren Emulgel", "50g", 32.90, 30),
    ("PR4424", "Counterpain Cream", "60g", 14.50, 45),
    ("PR2829", "Salonpas Patch", "20 pcs", 15.90, 70),
    ("PR4802", "Tiger Balm White", "19.4g", 8.90, 100),
    # Cough & Cold
    ("CC7396", "Strepsils Honey Lemon", "24 pcs", 15.90, 45),
    ("CC6925", "Woods Peppermint Syrup", "100ml", 12.50, 40),
    ("CC1715", "Difflam Lozenges", "16 pcs", 14.90, 35),
    ("CC4253", "Clarinase Repetabs", "10 pcs", 24.90, 25),
    ("CC5664", "Actifed Syrup", "100ml", 16.50, 30),
    ("CC7915", "Breacol Cough Syrup", "120ml", 11.90, 40),
    ("CC9257", "Vicks VapoRub", "50g", 13.50, 55),
    ("CC3977", "Fisherman's Friend", "25g", 4.90, 80),
    ("CC8006", "Otrivin Nasal Spray", "10ml", 18.90, 30),
    ("CC3602", "Panadol Cold & Flu", "12 pcs", 9.90, 60),
    # Allergy
    ("AL3920", "Zyrtec 10mg", "10 pcs", 19.90, 35),
    ("AL3845", "Clarityne 10mg", "10 pcs", 22.50, 30),
    ("AL4036", "Telfast 120mg", "10 pcs", 26.90, 25),
    ("AL5257", "Aerius 5mg", "10 pcs", 27.50, 20),
    ("AL4616", "Piriton 4mg", "30 pcs", 8.90, 50),
    ("AL1159", "Zyrtec Syrup", "60ml", 21.90, 25),
    ("AL3349", "Opticrom Eye Drops", "10ml", 19.50, 20),
    ("AL1767", "Flixonase Nasal Spray", "60 doses", 38.90, 15),
    ("AL9858", "Calamine Lotion", "100ml", 7.90, 40),
    ("AL3816", "Benadryl Allergy", "12 pcs", 14.90, 30),
    # Digestive
    ("DG5057", "Gaviscon Double Action", "12 pcs", 16.90, 40),
    ("DG4209", "Eno Fruit Salt", "6 sachets", 6.90, 60),
    ("DG5073", "Gaviscon Liquid", "150ml", 19.90, 30),
    ("DG7198", "Buscopan 10mg", "20 pcs", 18.50, 35),
    ("DG1247", "Imodium 2mg", "6 pcs", 12.90, 40),
    ("DG5780", "Dulcolax 5mg", "10 pcs", 10.90, 45),
    ("DG6138", "Smecta", "10 sachets", 15.90, 30),
    ("DG4168", "Activated Charcoal", "30 pcs", 9.50, 35),
    ("DG3700", "Polycrol Gel", "180ml", 13.90, 25),
    ("DG6427", "Hydrolyte Sachets", "10 sachets", 11.50, 50),
    # Vitamins & Supplements
    ("VS4258", "Redoxon Vitamin C 1000mg", "15 pcs", 29.90, 50),
    ("VS8045", "Blackmores Fish Oil", "60 pcs", 45.00, 25),
    ("VS7695", "Centrum Multivitamin", "30 pcs", 39.90, 30),
    ("VS4369", "Appeton Multivitamin", "60 pcs", 32.50, 35),
    ("VS1341", "Berocca Performance", "15 pcs", 27.90, 40),
    ("VS6643", "Caltrate Plus", "60 pcs", 49.90, 20),
    ("VS8737", "Vitamin D3 1000IU", "60 pcs", 24.90, 30),
    ("VS5861", "Neurobion", "30 pcs", 21.90, 35),
    ("VS3437", "Scott's Emulsion", "200ml", 28.50, 25),
    ("VS6403", "Zinc Gluconate 50mg", "60 pcs", 18.90, 40),
    # First Aid
    ("FA5684", "Dettol Antiseptic Liquid", "250ml", 14.90, 40),
    ("FA6644", "Hansaplast Plasters", "20 pcs", 6.50, 100),
    ("FA9942", "Betadine Solution", "60ml", 12.90, 35),
    ("FA8731", "Elastoplast Fabric", "40 pcs", 11.90, 50),
    ("FA9690", "Crepe Bandage 7.5cm", "1 roll", 5.50, 45),
    ("FA4443", "Gauze Swabs", "10 pcs", 3.90, 80),
    ("FA6785", "Micropore Tape", "1 roll", 4.90, 60),
    ("FA5184", "Burnol Cream", "20g", 8.50, 30),
    ("FA7256", "Alcohol Swabs", "100 pcs", 7.90, 70),
    ("FA7076", "Cold Pack", "1 pc", 9.90, 25),
]
# Medicine ID
CATEGORY_CODES = {
    "PR": "Pain Relief",
    "CC": "Cough & Cold",
    "AL": "Allergy",
    "DG": "Digestive",
    "VS": "Vitamins & Supplements",
    "FA": "First Aid",
}
CODE_LENGTH = 2
NUMBER_LENGTH = 4
ID_LENGTH = CODE_LENGTH + NUMBER_LENGTH

# Hash table
HASH_TABLE_SIZE = 101
HASH_BASE = 37
MAX_LOAD_FACTOR = 0.7

# Display
PROMPT_WIDTH = 24
DISPLAY_WIDTH = 50
CODE_COLUMN_WIDTH = 7
CATEGORY_COLUMN_WIDTH = 36
LABEL_WIDTH = 15

# Benchmark
SEARCH_REPEATS = 10000

# Search experiment
DATASET_SIZES = (60, 5000, 50000)  # Small (the sample medicines), intermediate, large
MISSING_ID = "PR0000"  # Never stored, since item numbers start from 0001
POSITION_WIDTH = 9
ID_WIDTH = 8
TIME_WIDTH = 12
SPEED_UP_WIDTH = 9
