#!/bin/bash

# GSMG.IO Puzzle Password Tester
# Tests passwords against the SalPhaselon AES blob

BLOB_FILE="salphaselon_blob.txt"
RESULTS_FILE="password_test_results.txt"

# Function to test a password
test_password() {
    local pass="$1"
    local mode="$2"

    # Try with different digest modes
    for digest in "" "-md md5" "-md sha256" "-md sha1" "-md sha512"; do
        result=$(openssl enc -aes-256-cbc -d -a $digest -in "$BLOB_FILE" -pass "pass:$pass" 2>&1)
        if [[ $? -eq 0 ]] && [[ ! "$result" =~ "bad decrypt" ]] && [[ ! "$result" =~ "error" ]]; then
            echo "SUCCESS with password: $pass (digest: $digest)" | tee -a "$RESULTS_FILE"
            echo "Result: $result" | tee -a "$RESULTS_FILE"
            echo "---" | tee -a "$RESULTS_FILE"
            return 0
        fi
    done
    return 1
}

# Function to test a SHA256 hash of a password
test_sha256() {
    local input="$1"
    local hash=$(echo -n "$input" | sha256sum | cut -d' ' -f1)
    test_password "$hash" "sha256($input)"
}

echo "Starting password testing at $(date)" | tee "$RESULTS_FILE"
echo "=======================================" | tee -a "$RESULTS_FILE"

# Count of passwords tested
count=0

# === MATRIX QUOTES ===
passwords=(
    # Architect's last words variations
    "sheisgoingtodieandthereisnothingthatyoucandotostopit"
    "sheisgoingtodieandthereisnothingyoucandotostopit"
    "sheisgoingtodiethereisnothingcandostopit"
    "sheisgoingtodienothingcandostopit"
    "sheisgoingtodieandthereisnothingicandotostopit"
    "sheisgoingtodieandthereisnothingonecanstopthis"
    "sheisdyingnothingcanstopthis"
    "sheisdyingnothingcanstopit"

    # Neo's quotes
    "theproblemischoice"
    "choiceistheproblem"
    "choice"
    "theproblem"
    "choicetheproblem"
    "choicetheproblemischoice"

    # Architect quotes
    "hope"
    "hopeitisthequintessentialhumandelusion"
    "hopethequintessentialhumandelusion"
    "quintessentialhumandelusion"
    "denial"
    "denialismostpredictable"
    "denialismostpredictableofallhumanresponses"
    "thefunctionoftheone"
    "thefunctionoftheoneisnowtoreturntotheSource"
    "returntotheSource"
    "thesource"
    "theSource"
    "Source"
    "source"

    # The problem is choice related
    "asadequatelyputtheproblemischoice"
    "adequatelyputtheproblemischoice"
    "wewontwewont"
    "wewillnotwe"
    "ifiwereuwouldhopewewontmeetagain"
    "wewont"

    # Oracle quotes
    "makechoice"
    "alreadymadechoice"
    "youhavealreadymadechoice"
    "youhavetounderstandit"

    # Morpheus quotes
    "everythingbeginswithchoice"
    "freeyourmind"
    "wakeupneo"
    "welcometotherealworld"
    "thematrixhasyou"
    "thereisadifferencebetweenknowingthepathandwalkingthepath"

    # Matrix numbers/elements
    "23"
    "16"
    "7"
    "23167"
    "16723"
    "71623"
    "16female7male"
    "23individuals"

    # Door choice related
    "leftdoor"
    "rightdoor"
    "theleftdoor"
    "therightdoor"
    "doorontheleft"
    "doorontheright"
    "choiceofdoor"
    "doorchoice"
    "neoschoice"
    "neochoosesleft"
    "choosetheleftdoor"

    # Causality variations
    "causality"
    "causeandefffect"
    "causeandeffect"
    "theresourcewillbringtheprogramback"

    # Decoded elements raw
    "matrixsumlist"
    "enter"
    "lastwordsbeforearchichoice"
    "thispassword"
    "matrixsumlistenter"
    "entermatrixsumlist"
    "lastwordsbeforearchichoicethispassword"
    "thispasswordlastwordsbeforearchichoice"

    # All decoded concatenated
    "matrixsumlistenterlastwordsbeforearchichoicethispassword"
    "matrixsumlistenterthispassword"
    "enterlastwordsbeforearchichoice"

    # First hint variations
    "theseedisplanted"
    "gsmg.io/theseedisplanted"
    "seedisplanted"
    "theseed"
    "seedplanted"
    "plantedtheseed"
    "theseedhasbeenplanted"

    # Hash the text
    "HASHTHETEXT"
    "hashthetext"
    "Hashthetext"
    "HashTheText"
    "hashtexthash"

    # Archimedes related
    "noliturbarecirculosmeos"
    "donotdisturbmycircles"
    "dontdisturbmycircles"
    "eureka"
    "givemeleverandicanmovetheworld"
    "archimedes"
    "Archimedes"

    # Architecture/archi variations
    "archi"
    "architect"
    "Architect"
    "ARCHITECT"
    "thearchitect"
    "TheArchitect"
    "architectschoice"
    "architektschoice"
    "archichoice"
    "archchoice"

    # Half and better half
    "halfandbetterhalf"
    "halfbetterhalf"
    "thehalf"
    "betterhalf"
    "halfandhalf"
    "thehalfandbetterhalf"
    "halfbetter"
    "betterhalf"

    # Previous phase passwords
    "theflowerblossomsthroughwhatseemstobeaconcretesurface"
    "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    "THEMATRIXHASYOU"

    # Logic / The Warning
    "thewarning"
    "TheWarning"
    "logic"
    "Logic"
    "theflowerblossoms"

    # Chess related
    "buddhist"
    "buddhistmove"
    "nomatemove"
    "nocheckmate"

    # Bitcoin/crypto related
    "satoshi"
    "nakamoto"
    "satoshinakamoto"
    "bitcoin"
    "genesisblock"
    "genesis"

    # Numbers and sums
    "422"
    "100110001001"
    "57757457637125"
    "575774576371252"
    "2441"
    "57+75+74+57+63+71+25"
    "57,75,74,57,63,71,25"

    # JFK / Executive Order
    "11110"
    "ExecutiveOrder11110"
    "executiveorder11110"
    "EO11110"
    "eo11110"

    # Luna/Safenet/HSM
    "SafenetLunaHSM"
    "safenetlunahsm"
    "SAFENETLUNAHSM"
    "luna"
    "Luna"
    "LUNA"
    "safenet"
    "Safenet"
    "SAFENET"
    "hsm"
    "HSM"

    # Combined passwords from phases
    "causalitySafenetLunaHSM"
    "causality11110"

    # Shabef related
    "shabef"
    "sha256"
    "SHA256"
    "shabefanstoo"
    "sha256answertoo"

    # Your last command
    "yourlastcommand"
    "lastcommand"
    "firsthint"
    "ourfirsthint"
    "firsthintisyourlastcommand"
    "ourfirsthintisyourlastcommand"

    # Second answer
    "secondanswer"
    "thesecondanswer"
    "answer2"
    "answertwo"

    # Combinations of decoded elements
    "matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlistyourlastcommandsecondanswer"

    # White rabbit
    "whiterabbit"
    "followthewhiterabbit"
    "rabbit"
    "whiterabbitseverywhere"

    # Merovingian quotes
    "choiceisanillusion"
    "choiceisanillusioncreatedbetweenthosewithpowerandthosewithout"
    "averyspecialdessert"
    "iwroteitmyself"

    # Keymaker
    "keymaker"
    "thekeymaker"
    "key"
    "thekey"

    # Oracle/Neo/Trinity
    "neo"
    "trinity"
    "morpheus"
    "oracle"
    "theoracle"
    "zion"
    "Zion"

    # Smith quotes
    "mrAnderson"
    "mranderson"
    "MrAnderson"
    "anderson"
    "purpose"
    "inevitability"

    # Cosmic duality
    "cosmicduality"
    "duality"
    "cosmic"
    "CosmicDuality"

    # Salphaselon
    "salphaselon"
    "Salphaselon"
    "SalPhaselon"
    "SALPHASELON"
    "salphaseion"
    "SalPhaseIon"

    # GSMG related
    "gsmg"
    "GSMG"
    "gsmgio"
    "GSMGIO"
    "5btc"
    "5BTC"
    "gsmgio5btc"
    "GSMGIO5BTC"

    # Puzzle address
    "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

    # Various combinations
    "youaretheone"
    "theone"
    "iamtheone"
    "thereisnoSpoon"
    "thereisnospoon"
    "nospoon"
    "spoon"

    # Fluidity/future
    "thefutureisfluid"
    "futureisfluid"
    "thefutureisours"
    "futureisours"
    "eachact"
    "eachdecision"

    # Heisenberg
    "heisenberg"
    "uncertaintyprinciple"
    "heisenbergsuncertaintyprinciple"
    "heisenberguncertainty"

    # Alice in Wonderland
    "howlongisforever"
    "sometimesjustonesecond"
    "justonesecond"
    "onesecond"
    "forever"
    "giveit"
    "giveitjustonesecond"

    # Jacque Fresco
    "jacquefresco"
    "JacqueFresco"
    "JACQUEFRESCO"
    "fresco"
    "Fresco"

    # Red/blue pill
    "redpill"
    "bluepill"
    "redorblue"
    "taketheRedpill"
    "taketheredpill"
    "redpillorbluepill"

    # Simple stuff
    "password"
    "Password"
    "PASSWORD"
    "puzzle"
    "Puzzle"
    "PUZZLE"
    "solution"
    "answer"
    "secret"
    "private"
    "privatekey"
    "key"

    # Anomaly
    "anomaly"
    "theanomaly"
    "youaretheanomaly"
    "systemicanomaly"

    # Code/program
    "theprimeprogram"
    "primeprogram"
    "prime"
    "code"
    "thecode"
    "matrix"
    "thematrix"
    "Matrix"
    "TheMatrix"
    "THEMATRIX"

    # Cataclysmic
    "cataclysmic"
    "cataclysmicessystemcrash"
    "systemcrash"

    # Numbers spelled
    "twenty three"
    "twentythree"
    "sixteen"
    "seven"
    "sixteenandseven"

    # Beaufort
    "beaufort"
    "Beaufort"
    "BEAUFORT"
    "beautiful"
    "beautifulstrategicposition"

    # EBCDIC
    "1141"
    "ibm1141"
    "IBM1141"
    "ebcdic1141"
    "EBCDIC1141"

    # Binary patterns
    "01100111"
    "01110011"
    "11110"
    "11111"

    # Norton/Thevenin
    "norton"
    "nortontheorem"
    "thevenin"

    # VIC cipher related
    "vic"
    "viccpher"
    "FUBCDORA"
    "fubcd"
    "FUBCD"

    # Last words variations
    "lastwords"
    "lastwordsbeforechoice"
    "wordsbeforechoice"
    "beforechoice"
    "beforethechoice"

    # Architect + choice
    "architectbeforechoice"
    "architectslastwords"
    "lastwordsofarchitect"
    "architectswords"

    # Destruction/creation
    "destruction"
    "creation"
    "balance"
    "equilibrium"

    # Faith/belief
    "believe"
    "faith"
    "trust"
    "ibelieve"

    # Simple numeric
    "123456"
    "12345678"
    "1234567890"
    "0987654321"

    # More Matrix deep cuts
    "trainman"
    "thetrainman"
    "mobil"
    "mobilave"
    "sati"
    "seraph"
    "niobe"
    "locksmith"
    "councilor"
    "hamann"
    "counselorhamann"

    # Encryption keywords
    "aes256cbc"
    "AES256CBC"
    "aes-256-cbc"
    "openssl"
    "encrypt"
    "decrypt"

    # Control/power
    "control"
    "power"
    "thosewithpower"
    "thosewithoutpower"

    # Illusion
    "illusion"
    "realityisanillusion"
    "theillusion"

    # Systems
    "system"
    "thesystem"
    "systematicAnomaly"

    # Greek words
    "arche"
    "archē"
    "logos"
    "telos"

    # More combinations
    "matrixsum"
    "sumlist"
    "listsum"
    "matrixlist"
    "listmatrix"
    "summatrix"

    # Raw matrix values
    "dbbibtbhcc"
    "dbbibfbhcc"

    # Crypto stuff
    "sha256answer"
    "sha256password"
    "aespassword"
    "aeskey"

    # Row sums direct
    "5775745763712"
    "57757457637125"
    "5775745763712500"

    # More archimedes
    "circles"
    "mycircles"
    "disturbmycircles"
    "donotdisturb"

    # Stand away
    "standaway"
    "standawayfellow"
    "standawayfellowfrommydiagram"
    "mydiagram"
    "diagram"

    # Greek/latin
    "nolitubare"
    "circulos"
    "meos"

    # Additional Matrix
    "knowthyself"
    "teutoniacaeli"
    "knowyourself"

    # Simulation
    "simulation"
    "simulacra"
    "baudrillard"

    # Philosophy
    "descartes"
    "cogito"
    "cogitoergosum"
    "iamwhoiam"
    "existentialism"

    # Binary choices
    "zeroone"
    "01"
    "10"
    "binaryChoice"
    "binarychoice"

    # Duality concepts
    "yinyang"
    "lightdark"
    "goodevil"
    "choicefreewill"

    # VIC cipher digits
    "14"
    "41"
    "digit14"
    "digit41"

    # Trying different capitalizations of key phrases
    "MATRIXSUMLIST"
    "ENTER"
    "LASTWORDSBEFOREARCHICHOICE"
    "THISPASSWORD"
    "Matrixsumlist"
    "LastWordsBeforeArchiChoice"
    "ThisPassword"

    # Trying spaceless versions of Architect quotes
    "failuretocomplywithprocessresultcataclysmicessystemcrash"
    "returntosourceallowtemporarydissemination"
    "functionofonereturntosource"

    # More door variations
    "twodoors"
    "doorright"
    "doorleft"
    "rightleft"
    "leftrightdoor"

    # Numbered items
    "23ciphers"
    "16encryptions"
    "7passwords"
    "23ciphers16encryptions7passwords"

    # Exact quote fragments
    "asadequately"
    "adequately"
    "adequatelyput"

    # "We won't" ending
    "wewont"
    "hopewedontmeetagain"
    "wewillnotmeetagain"

    # Already know variations
    "wealreadyknow"
    "wealreadyknowwhatyouaregoingto"
    "wealreadyknowwhatyouwilldo"
    "weknow"
    "youknow"
    "iknow"

    # Blind variations
    "blind"
    "blinded"
    "blindedbylove"
    "blindedbyanemotion"
    "anemotionthatisblindingyou"
    "emotionthatisblindingyou"

    # Trinity related
    "saveTrinity"
    "savetrinity"
    "lovedone"
    "love"
    "trinity"
    "neolovestrinity"
    "neoandtrinity"

    # Simple/obvious truth
    "simpleobvioustruth"
    "thetruth"
    "truth"
    "obvious"
    "obvioustruth"

    # Going to die
    "goingtoDie"
    "goingtodiethereisnothingicando"
    "nothingicando"
    "nothingcando"
    "cantprevent"
    "cannotstopdeath"

    # Salvation/zion
    "salvationofzion"
    "savezion"
    "zionsalvation"

    # End of species
    "endofspecies"
    "endofhumanrace"
    "humanrace"
    "extinction"
    "extermination"

    # Matrix as prison
    "prison"
    "theprison"
    "escapethematrix"
    "escape"

    # Program related
    "program"
    "primeprogram"
    "reinserting"
    "reinsertingprime"
    "reinsertion"

    # 6 predecessors
    "sixpredecessors"
    "predecessors"
    "sixthone"
    "theFirst"
    "theSixth"

    # Equation/balance
    "equation"
    "unbalancedequation"
    "remainder"
    "sumremainder"

    # Your life
    "yourlife"
    "yourlifeisthesum"
    "sumremainder"
    "remainderofunbalanced"

    # Concordantly
    "concordantly"
    "ergo"
    "ergoconcordantly"
    "vis-a-vis"

    # Integers to strings
    "one"
    "two"
    "three"
    "four"
    "five"
    "six"
    "zero"

    # Raw letter grid sample
    "dbbibfbhccbegbihab"
    "faedggee"
    "dfcbdabhh"
)

echo "Testing ${#passwords[@]} password variations..." | tee -a "$RESULTS_FILE"

for pass in "${passwords[@]}"; do
    ((count++))
    # Test raw password
    test_password "$pass"

    # Test SHA256 of password
    test_sha256 "$pass"

    # Progress indicator every 50
    if (( count % 50 == 0 )); then
        echo "Tested $count passwords so far..."
    fi
done

echo "" | tee -a "$RESULTS_FILE"
echo "Testing SHA256 hashes directly as passwords..." | tee -a "$RESULTS_FILE"

# Known SHA256 hashes
sha256_hashes=(
    "e7546e3076294907ed2a0ecaa9c33062f6e602b7c74c5aa5cc865df0ff345507"  # SHA256(matrixsumlist)
    "e08d706b3e4ce964b632746cf568913cb93f1ed36476fbb0494b80ed17c5975c"  # SHA256(enter)
    "77094e7a1591fb81379f1582cf88db5aa6ab8e77176a4d8428a1ff5decfd102d"  # SHA256(lastwordsbeforearchichoice)
    "74c1d7592daf4f89b0a7ba5e368bb59cc9e19c6a4ebb7f33cd8ccf8f3edacac0"  # SHA256(thispassword)
    "5968dc5e02cbdf8181d135f143372e7062504cc06268e094ceae25b56c5a72ae"  # SHA256(HASHTHETEXT)
    "6e3f5a7baf924d8546f5f7af94a43b8424e3c810983f9795eb8451ad4243d860"  # SHA256(theseedisplanted)
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf"  # SHA256(causality)
    "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5"  # Phase 3.1 password
    "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"  # Phase 3.2 password
    "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"  # SHA256(puzzle text)
    "a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735"  # Seven-token XOR
    "4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081"  # Claimed cosmic duality output
)

for hash in "${sha256_hashes[@]}"; do
    ((count++))
    test_password "$hash"
done

echo "" | tee -a "$RESULTS_FILE"
echo "Testing XOR combinations..." | tee -a "$RESULTS_FILE"

# Try using the key/IV from Issue #55 directly
echo "Testing direct key/IV from Issue #55..." | tee -a "$RESULTS_FILE"
result=$(openssl enc -aes-256-cbc -d -a -K "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23" -iv "c6ff2e39d98843bc3c26b8a33a15b5c9" -in "$BLOB_FILE" 2>&1)
if [[ $? -eq 0 ]]; then
    echo "SUCCESS with direct key/IV!" | tee -a "$RESULTS_FILE"
    echo "Result: $result" | tee -a "$RESULTS_FILE"
fi

echo "" | tee -a "$RESULTS_FILE"
echo "Completed testing $count passwords at $(date)" | tee -a "$RESULTS_FILE"
echo "Check $RESULTS_FILE for any successful decryptions" | tee -a "$RESULTS_FILE"
