#!/bin/bash
set -e

SEED_DIR=${SEED_DIR:-./data}

fix_deltamax(){
    # deltaMAX BPM
    sed -i "" "s/#BPMS.*/#BPMS:0=100.05,4=100,20=101,21=102,22=103,23=104,24=105,25=106,26=107,27=108,28=109,29=110,30=111,31=112,32=113,33=114,34=115,35=116,36=117,37=118,38=119,39=120,40=121,41=122,42=123,43=124,44=125,45=126,46=127,47=128,48=129,49=130,50=131,51=132,52=133,54=135,55=136,56=137,57=138,58=139,59=140,60=141,61=142,62=143,63=144,64=145,65=146,66=147,67=148,68=149,69=150,70=151,71=152,72=153,73=154,74=155,75=156,76=157,77=158,78=159,79=160,80=161,81=162,82=163,83=164,84=165,85=166,86=167,87=168,88=169,89=170,90=171,91=172,93=174,94=175,95=176,96=177,97=178,98=179,99=180,100=181,101=182,102=183,103=184,104=185,105=186,106=187,107=188,108=189,109=190,110=191,111=192,112=193,113=194,114=195,115=196,116=197,117=198,118=199,119=200,120=201,121=202,122=203,123=204,124=205,125=206,126=207,127=208,128=209,129=210,130=211,131=212,132=213,133=214,134=215,135=216,136=217,137=218,138=219,139=220,140=221,141=222,142=223,143=224,144=225,145=226,146=227,147=228,148=229,149=230,150=231,151=232,152=233,153=234,154=235,155=236,156=237,157=238,158=239,159=240,160=241,161=242,162=243,163=244,164=245,165=246,166=247,167=248,168=249,169=250,170=251,171=252,172=253,173=254,174=255,175=256,176=257,177=258,178=259,179=260,180=261,181=262,182=263,183=264,184=265,185=266,186=267,187=268,188=269,189=270,190=271,191=272,192=273,193=274,194=275,195=276,196=277,197=278,198=279,199=280,200=281,201=282,202=283,203=284,204=285,205=286,206=287,207=288,208=289,209=290,210=291,211=292,212=293,213=294,214=295,215=296,216=297,217=298,218=299,219=300,220=301,221=302,222=303,223=304,224=305,225=306,226=307,227=308,228=309,229=310,230=311,231=312,232=313,233=314,234=315,235=316,236=317,237=318,238=319,239=320,240=321,241=322,242=323,243=324,244=325,245=326,246=327,247=328,248=329,249=330,250=331,251=332,252=333,253=334,254=335,255=336,256=337,257=338,258=339,259=340,260=341,261=342,262=343,263=344,264=345,265=346,266=347,267=348,268=349,269=350,270=351,271=352,272=353,273=354,274=355,275=356,276=357,277=358,278=359,279=360,280=361,281=362,282=363,283=364,284=365,285=366,286=367,287=368,288=369,289=370,290=371,291=372,292=373,293=374,294=375,295=376,296=377,297=378,298=379,299=380,300=381,301=382,302=383,303=384,304=385,305=386,306=387,307=388,308=389,309=390,310=391,311=392,312=393,313=394,314=395,315=396,316=397,317=398,318=399,319=400,320=401,321=402,322=403,323=404,324=405,325=406,326=407,327=408,328=409,329=410,330=411,331=412,332=413,333=414,334=415,335=416,336=417,337=418,338=419,339=420,340=421,341=422,342=423,343=424,344=425,345=426,346=427,347=428,348=429,349=430,350=431,351=432,352=433,353=434,354=435,355=436,356=437,357=438,358=439,359=440,360=441,361=442,362=443,363=444,364=445,365=446,366=447,367=448,368=449,369=450,370=451,371=452,372=453,373=454,374=455,375=456,376=457,377=458,378=459,379=460,380=461,381=462,382=463,383=464,384=465,385=466,386=467,387=468,388=469,389=470,390=471,391=472,392=473,393=474,394=475,395=476,396=477,397=478,398=479,399=480,400=481,401=482,402=483,403=484,404=485,405=486,406=487,407=488,408=489,409=490,410=491,411=492,412=493,413=494,414=495,415=496,416=497,417=498,418=499,419=500,420=501,421=502,422=503,423=504,424=505,425=506,426=507,427=508,428=509,429=510,430=511,431=512,432=513,433=514,434=515,435=516,436=517,437=518,438=519,439=520,440=521,441=522,442=523,443=524,444=525,445=526,446=527,447=528,448=529,449=530,450=531,451=532,452=533,453=534,454=535,455=536,456=537,457=538,458=539,459=540,460=541,461=542,462=543,463=544,464=545,465=546,466=547,467=548,468=549,469=550,470=551,471=552,472=553,473=554,474=555,475=556,476=557,477=558,478=559,479=560,480=561,481=562,482=563,483=564,484=565,485=566,486=567,487=568,488=569,489=570,490=571,491=572,492=573;/g" "$SEED_DIR/X2/deltaMAX/deltaMAX.sm"
}

fix_koihadoumoro(){
    # sm file has ;new; which breaks parsing
    sed -i "" 's/;new;/;/' "$SEED_DIR/2014/Koi hadou Moro Hadou OK Houteishiki!!/Koi hadou Moro Hadou OK Houteishiki!!.sm"
}

fix_takemehigher(){
    ver="A20 PLUS"
    path="$SEED_DIR/$ver"

    old_name="take me higher"
    new_name="take me higher A20P"

    if [[ -d "$path/$old_name" ]]; then
        echo renaming "$path/$old_name" to "$path/$new_name"
        cd "$path"
        rm -vrf "$new_name"
        mkdir -p "$new_name"
        cp -R "$old_name"/ "$new_name"/
        cd "$new_name"
        rename -v "s/$old_name/$new_name/" *.* && echo "done";
        rm -vrf "$path/$old_name"
    fi
}

fix_deltamax
fix_takemehigher
fix_koihadoumoro
