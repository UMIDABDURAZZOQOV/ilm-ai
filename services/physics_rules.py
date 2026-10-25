"""Reviewed grade-six formula families and independent SI arithmetic oracles.

No runtime evaluation of the submitted formula, no general CAS/equivalence
claim. Each alternative has a stated source domain. The content validator
recalculates answers from structured givens, independently of stored answers.
"""

from fractions import Fraction

from services.assessment_grading import UNITS, numeric


def rule(target, variables, equivalents, conditions):
    return {
        "target": target,
        "variables": variables,
        "equivalents": equivalents,
        "conditions": conditions,
    }


REVIEWED_FORMULAS = {
    "orbit_altitude": rule(
        "h",
        ["v", "g", "R"],
        ["v^2/g-R", "v*v/g-R"],
        "Ideal aylana orbita,g ayni orbitada,h>=0;7sinfPDF105.",
    ),
    "static_balance": rule(
        "f",
        ["F", "Fmax"],
        ["F", "1*F"],
        "Gorizontal tinch muvozanat,0<=F<=Fmax; Fmax berilgan chegaraviy modul;7sinfPDF108–111.",
    ),
    "sliding_force": rule(
        "f",
        ["mu", "N"],
        ["mu*N", "N*mu"],
        "Sirpanayotgan sirtlar oddiy Coulomb modeli,N>0,mu>=0;7sinfPDF112.",
    ),
    "sliding_coefficient": rule(
        "mu",
        ["f", "N"],
        ["f/N", "f*N^-1"],
        "Sirpanishda f>=0,N>0; birliksiz;7sinfPDF112.",
    ),
    "rolling_force": rule(
        "f",
        ["c", "P", "r"],
        ["c*P/r", "P*c/r"],
        "Kitob dumalash modeli,c uzunlik birligida,P>0,r>0;7sinfPDF114.",
    ),
    "sliding_lab_mu": rule(
        "mu",
        ["F", "m", "g"],
        ["F/(m*g)", "F/m/g"],
        "Gorizontal tekis tortish,vertikal a0, F sirpanish kuchi,g10berilgan;7sinfPDF112,115–116.",
    ),
    "mean_mu3": rule(
        "mu_ort",
        ["mu1", "mu2", "mu3"],
        ["(mu1+mu2+mu3)/3", "mu1/3+mu2/3+mu3/3"],
        "Bir xil sirtlar juftining uch sirpanish koeffitsiyenti;7sinfPDF116.",
    ),
    "gravity_pair": rule(
        "F",
        ["G", "m1", "m2", "r"],
        ["G*m1*m2/r^2", "G*m2*m1/(r*r)"],
        "Moddiy nuqtalar yoki sferik taqsimotli jismlar, markazlar oralig‘i r>0,G=6.67e-11;7sinfPDF90–93.",
    ),
    "gravity_force7": rule(
        "F",
        ["m", "g"],
        ["m*g", "g*m"],
        "Yer yaqinida masalada g=9.8 yoki10m/s2 berilgan, m>0;7sinfPDF94–95.",
    ),
    "gravity_mass7": rule(
        "m", ["F", "g"], ["F/g", "F*g^-1"], "F>0,g=9.8 yoki10m/s2 berilgan;7sinfPDF95."
    ),
    "rest_weight": rule(
        "P",
        ["m", "g"],
        ["m*g", "g*m"],
        "Tayanch/osma bilan vertikal a=0, g=9.8 yoki10m/s2;7sinfPDF96–98.",
    ),
    "apparent_up": rule(
        "P",
        ["m", "g", "a"],
        ["m*(g+a)", "m*g+m*a"],
        "Tayanch bilan yuqoriga a>=0 tezlanish, doimiyg9.8/10;7sinfPDF98–101.",
    ),
    "apparent_down": rule(
        "P",
        ["m", "g", "a"],
        ["m*(g-a)", "m*g-m*a"],
        "Pastga a moduli 0<=a<=g; kontakt mavjud yoki freefall a=g;7sinfPDF99–100.",
    ),
    "load_factor": rule(
        "n",
        ["g", "a"],
        ["(g+a)/g", "1+a/g"],
        "Yuqoriga tezlanishdagi P/mg, g9.8/10,a>=0;7sinfPDF98.",
    ),
    "horizontal_range": rule(
        "s",
        ["v0", "t"],
        ["v0*t", "t*v0"],
        "Havosiz, gorizontal boshlang‘ich tezlik, bir xil oraliq t>=0;7sinfPDF102–105.",
    ),
    "horizontal_drop": rule(
        "h",
        ["g", "t"],
        ["g*t^2/2", "0.5*g*t*t"],
        "Vertikal v0=0,h pastga tushilgan masofa,doimiyg9.8/10;7sinfPDF102–105.",
    ),
    "altitude_gravity": rule(
        "gh",
        ["G", "M", "R", "h"],
        ["G*M/(R+h)^2", "G*M/((R+h)*(R+h))"],
        "Sferik Yer modeli,R,M>0,h>=0,G=6.67e-11;7sinfPDF103.",
    ),
    "orbital_radius": rule(
        "r",
        ["v", "g"],
        ["v^2/g", "v*v/g"],
        "Ideal aylana orbita,v>0,g ayni orbitada,R=v²/g;7sinfPDF104.",
    ),
    "newton_acceleration": rule(
        "a",
        ["F", "m"],
        ["F/m", "F*m^-1"],
        "F natijaviy kuch moduli,m>0,klassik/inersial;7sinfPDF73–74.",
    ),
    "newton_force": rule(
        "F",
        ["m", "a"],
        ["m*a", "a*m"],
        "Natijaviy kuch moduli, m>0,a>=0;7sinfPDF73–74.",
    ),
    "newton_mass": rule(
        "m",
        ["F", "a"],
        ["F/a", "F*a^-1"],
        "F>0,a>0 klassik inersial model;7sinfPDF73–74.",
    ),
    "reaction_magnitude": rule(
        "F2",
        ["F1"],
        ["F1", "1*F1"],
        "Turli jismlardagi ta’sir/aks ta’sir modullari, yo‘nalishlar teskari;7sinfPDF75–78.",
    ),
    "paired_acceleration": rule(
        "a2",
        ["m1", "a1", "m2"],
        ["m1*a1/m2", "a1*m1/m2"],
        "Faqat o‘zaro kuch ta’siridan tezlanish modullari, m1,m2>0;7sinfPDF78.",
    ),
    "centripetal_force": rule(
        "F",
        ["m", "v", "R"],
        ["m*v^2/R", "m*v*v/R"],
        "Natijaviy markazga kuch moduli, tekis aylana,m,R>0;7sinfPDF80.",
    ),
    "spring_force": rule(
        "F",
        ["k", "x"],
        ["k*x", "x*k"],
        "Kichik chiziqli elastik deformatsiya moduli x>=0,k>0;7sinfPDF83–85.",
    ),
    "spring_stiffness": rule(
        "k",
        ["F", "x"],
        ["F/x", "F*x^-1"],
        "Chiziqli elastik branch, F>0,x>0;7sinfPDF84–85.",
    ),
    "spring_extension": rule(
        "x",
        ["F", "k"],
        ["F/k", "F*k^-1"],
        "Chiziqli elastik branch, F>=0,k>0;7sinfPDF83–85.",
    ),
    "rod_stiffness": rule(
        "k",
        ["E", "S", "l"],
        ["E*S/l", "S*E/l"],
        "Bir jinsli sterjenning kichik aksial deformatsiyasi,E,S,l>0;7sinfPDF84.",
    ),
    "lab_stiffness": rule(
        "k",
        ["m", "g", "x"],
        ["m*g/x", "g*m/x"],
        "Tinch muvozanatdagi raqamli lab,g=10m/s2 berilgan,x,m>0;7sinfPDF86.",
    ),
    "mean_stiffness3": rule(
        "k_ort",
        ["k1", "k2", "k3"],
        ["(k1+k2+k3)/3", "k1/3+k2/3+k3/3"],
        "Bitta prujinaning uch musbat qaydidan o‘rtacha;7sinfPDF86–87.",
    ),
    "rotational_linear": rule(
        "v",
        ["omega", "R"],
        ["omega*R", "R*omega"],
        "Tekis aylanish, R>0, omega rad/s;7sinfPDF52.",
    ),
    "rotation_period": rule(
        "T",
        ["t", "n"],
        ["t/n", "t*n^-1"],
        "n musbat butun aylanishlar soni,t>0;7sinfPDF53.",
    ),
    "rotation_frequency": rule(
        "nu",
        ["n", "t"],
        ["n/t", "n*t^-1"],
        "n musbat butun aylanishlar soni,t>0;7sinfPDF53–54.",
    ),
    "angular_from_period": rule(
        "omega",
        ["p", "T"],
        ["2*p/T", "2*p*T^-1"],
        "p=3.14 ochiq yaqinlashuv,T>0;7sinfPDF53–54.",
    ),
    "centripetal": rule(
        "ac",
        ["v", "R"],
        ["v^2/R", "v*v/R"],
        "Chiziqli tezlik moduli v, aylana radiusi R>0;7sinfPDF56–57.",
    ),
    "centripetal_radius": rule(
        "R", ["v", "ac"], ["v^2/ac", "v*v/ac"], "v>0,ac>0;7sinfPDF57,10-mashq."
    ),
    "force_sum2": rule(
        "F",
        ["F1", "F2"],
        ["F1+F2", "F2+F1"],
        "Bir jismga bir yo‘nalishli kollinear kuchlar moduli;7sinfPDF64.",
    ),
    "force_difference": rule(
        "F",
        ["F1", "F2"],
        ["F1-F2"],
        "Kollinear qarama-qarshi kuchlar,F1>=F2; natija F1 yo‘nalishi;7sinfPDF64.",
    ),
    "mass_sum2": rule(
        "m",
        ["m1", "m2"],
        ["m1+m2", "m2+m1"],
        "Ikki qismli klassik jism, massalar bir birlikda;7sinfPDF71.",
    ),
    "accelerated_path": rule(
        "s",
        ["v0", "a", "t"],
        ["v0*t+a*t^2/2", "t*v0+0.5*a*t*t"],
        "Doimiy a, bir yo‘nalish, to‘xtashgacha;7sinfPDF37–39.",
    ),
    "lab_acceleration": rule(
        "a",
        ["s", "t"],
        ["2*s/t^2", "2*s/(t*t)"],
        "Tinch holatdan doimiy tezlanish, s>0,t>0;7sinfPDF40.",
    ),
    "mean_acceleration3": rule(
        "a_ort",
        ["a1", "a2", "a3"],
        ["(a1+a2+a3)/3", "a1/3+a2/3+a3/3"],
        "Bir xil qiya novning uch musbat qaydi;7sinfPDF40.",
    ),
    "fall_velocity": rule(
        "v",
        ["v0", "g", "t"],
        ["v0+g*t", "g*t+v0"],
        "Pastga musbat o‘q, havosiz, berilgan doimiyg;7sinfPDF42.",
    ),
    "fall_height": rule(
        "h",
        ["v0", "g", "t"],
        ["v0*t+g*t^2/2", "t*v0+0.5*g*t*t"],
        "Pastga tushish yo‘li, havo qarshiliksiz;7sinfPDF42.",
    ),
    "up_velocity": rule(
        "v",
        ["v0", "g", "t"],
        ["v0-g*t"],
        "Yuqoriga musbat; v ishorali proyeksiya, 0<=t<=2v0/g;7sinfPDF43–45.",
    ),
    "up_height": rule(
        "h",
        ["v0", "g", "t"],
        ["v0*t-g*t^2/2", "t*v0-0.5*g*t*t"],
        "Otilgan sathga nisbatan balandlik, jami yo‘l emas;0<=t<=2v0/g;7sinfPDF44–45.",
    ),
    "up_peak_time": rule(
        "t",
        ["v0", "g"],
        ["v0/g", "v0*g^-1"],
        "Yuqoriga otilishning cho‘qqigacha vaqti, v0>0;7sinfPDF44.",
    ),
    "arc_angle": rule(
        "phi",
        ["s", "R"],
        ["s/R", "s*R^-1"],
        "s yoy uzunligi (vatar emas), R>0; radian;7sinfPDF50–51.",
    ),
    "angular_speed": rule(
        "omega",
        ["phi", "t"],
        ["phi/t", "phi*t^-1"],
        "Tekis aylanish, phi radianlarda, t>0;7sinfPDF51.",
    ),
    "constant_acceleration": rule(
        "a",
        ["v", "v0", "t"],
        ["(v-v0)/t", "v/t-v0/t"],
        "Bir o‘qdagi musbat tezliklar, t>0; a ishorali proyeksiya;7sinfPDF31–33/bosma38–40.",
    ),
    "accelerated_velocity": rule(
        "v",
        ["v0", "a", "t"],
        ["v0+a*t", "a*t+v0"],
        "Doimiy ishorali a, t>=0, v0>=0; to‘xtashgacha v>=0 branch;7sinfPDF34–35/bosma41–42.",
    ),
    "linear_mean_speed": rule(
        "v_ort",
        ["v0", "v"],
        ["(v0+v)/2", "v0/2+v/2"],
        "Faqat doimiy tezlanish va yo‘nalish almashmasligi; ikkala endpoint tezlik>=0;7sinfPDF35–36/bosma42–43.",
    ),
    "codirectional_speed": rule(
        "v",
        ["v1", "v2"],
        ["v1+v2", "v2+v1"],
        "Klassik bir to‘g‘ri chiziq/bir yo‘nalish modeli; platforma Yerga, odam platformaga nisbatan;7sinfPDF2/bosma9.",
    ),
    "codirectional_length": rule(
        "s",
        ["a", "b"],
        ["a+b", "b+a"],
        "Ikki bir yo‘nalishli kollinear ko‘chish modullari;7sinfPDF13–14/bosma20–21.",
    ),
    "opposed_length": rule(
        "s",
        ["a", "b"],
        ["a-b"],
        "Qarama-qarshi kollinear ko‘chishlar, a>=b>=0; natija a yo‘nalishi bo‘yicha modul;7sinfPDF14/bosma21.",
    ),
    "scaled_length": rule(
        "s",
        ["a", "k"],
        ["a*k", "k*a"],
        "Ko‘chish vektorini musbat k songa ko‘paytirish, yo‘nalish saqlanadi;7sinfPDF14–15/bosma21–22.",
    ),
    "equal_intervals_distance": rule(
        "s",
        ["d", "n"],
        ["d*n", "n*d"],
        "Har teng vaqt oralig‘ida d yo‘l, n musbat butun oraliq;7sinfPDF20/bosma27.",
    ),
    "frequency_count": rule(
        "nu",
        ["n", "t"],
        ["n/t", "n*t^-1"],
        "n musbat butun tebranishlar soni, t>0 sekund; PDF157.",
    ),
    "echo_distance": rule(
        "h",
        ["v", "t"],
        ["v*t/2", "0.5*v*t"],
        "t borish-qaytish vaqti; bir xil muhitda v>0; h bir tomon masofa; PDF164.",
    ),
    "sound_absorption": rule(
        "alpha",
        ["Ea", "Ei"],
        ["Ea/Ei", "Ea*Ei^-1"],
        "Ei>0 tushgan,0<=Ea<=Ei yutilgan energiya, bir xil kuzatuv; PDF166.",
    ),
    "flat_image_distance": rule(
        "i",
        ["d"],
        ["d", "1*d"],
        "Yassi ko‘zgu: d>0 oldingi masofa, i orqadagi masofa moduli; PDF142–143.",
    ),
    "spherical_focus": rule(
        "F",
        ["R"],
        ["R/2", "0.5*R"],
        "Paraksial botiq sferik ko‘zgu modeli, R>0; PDF143 rasm/formula qutisi.",
    ),
    "concave_image": rule(
        "f",
        ["F", "d"],
        ["F*d/(d-F)", "1/(1/F-1/d)"],
        "Paraksial botiq ko‘zgu, F>0 va d>F; haqiqiy tasvir masofasi f>0; PDF144. d=F yoki virtual branch qabul qilinmaydi.",
    ),
    "lens_power": rule(
        "D",
        ["F"],
        ["1/F", "F^-1"],
        "Havodagi yig‘uvchi linza, F>0 metrlarda; D dioptriyada; PDF147.",
    ),
    "lens_focal": rule(
        "F",
        ["D"],
        ["1/D", "D^-1"],
        "Havodagi yig‘uvchi linza, D>0 dioptriyada; F metrlarda; PDF147.",
    ),
    "v_to_mv": rule(
        "y", ["x"], ["1000*x", "x*1000"], "x V, y mV; nonnegative magnitude, PDF126."
    ),
    "film_thickness": rule(
        "d",
        ["V", "S"],
        ["V/S", "V*S^-1"],
        "Bir molekulyar qatlam deb olingan bir tekis parda; S>0; V hajm, S yuza; PDF21. Bu model taxminiy.",
    ),
    "front_speed": rule(
        "v",
        ["h", "t"],
        ["h/t", "h*t^-1"],
        "h rangli qatlam siljishi, t>0 kuzatish vaqti; PDF28 dagi D≈h/t faqat shu kuzatuv ko‘rsatkichi, universal diffuziya koeffitsiyenti emas.",
    ),
    "kg_to_g": rule("y", ["x"], ["1000*x", "x*1000"], "x kg, y g; PDF30."),
    "g_to_kg": rule("y", ["x"], ["x/1000", "0.001*x"], "x g, y kg; PDF30."),
    "tonne_to_kg": rule("y", ["x"], ["1000*x", "x*1000"], "x t, y kg; PDF30."),
    "mass_sum3": rule(
        "m",
        ["m1", "m2", "m3"],
        ["m1+m2+m3"],
        "Muvozanatdagi tarozi: uch toshning massalari bir birlikda; PDF30–32.",
    ),
    "tare_mass": rule(
        "m",
        ["M", "m0"],
        ["M-m0"],
        "M idish va suvning umumiy massasi, m0 bo‘sh idish massasi, M>=m0; bir birlikda; PDF32.",
    ),
    "density": rule(
        "rho",
        ["m", "V"],
        ["m/V", "m*V^-1"],
        "Jismning o‘rtacha zichligi; m>0, V>0, mos massa va hajm birliklari; PDF33–35,37–38.",
    ),
    "density_mass": rule(
        "m", ["rho", "V"], ["rho*V", "V*rho"], "Bir jinsli jism: rho>0, V>0; PDF35."
    ),
    "density_volume": rule(
        "V", ["m", "rho"], ["m/rho", "m*rho^-1"], "Bir jinsli jism: rho>0, m>0; PDF35."
    ),
    "displacement": rule(
        "V",
        ["V2", "V1"],
        ["V2-V1"],
        "Jism to‘liq botgan, erimaydi, suv to‘kilmaydi, havo pufaklari yo‘q; V2>V1, bir hajm birligida; PDF34,37.",
    ),
    "box_volume": rule(
        "V",
        ["l1", "l2", "l3"],
        ["l1*l2*l3"],
        "To‘g‘ri burchakli parallelepipedning musbat o‘lchamlari bir uzunlik birligida; PDF37.",
    ),
    "km_to_m": rule("y", ["x"], ["1000*x", "x*1000"], "x km, y m; PDF47."),
    "min_to_s": rule("y", ["x"], ["60*x", "x*60"], "x minut, y sekund; PDF47."),
    "hour_to_s": rule("y", ["x"], ["3600*x", "x*3600"], "x soat, y sekund; PDF47."),
    "step_distance": rule(
        "s",
        ["l", "n"],
        ["l*n", "n*l"],
        "l o‘rtacha qadam uzunligi, n musbat butun qadamlar soni; taxminiy masofa; PDF48.",
    ),
    "motion_speed": rule(
        "v",
        ["s", "t"],
        ["s/t", "s*t^-1"],
        "s yo‘l, t>0 vaqt; tekis harakat tezligi yoki butun yo‘l/butun vaqt o‘rtachasi; PDF49–50.",
    ),
    "motion_distance": rule(
        "s",
        ["v", "t"],
        ["v*t", "t*v"],
        "v tekis harakat tezligi, t vaqt; yoki butun oraliqning berilgan o‘rtacha tezligi; PDF51.",
    ),
    "motion_time": rule(
        "t", ["s", "v"], ["s/v", "s*v^-1"], "s yo‘l, v>0 tezlik; PDF51,3-mashq7."
    ),
    "two_stage_speed": rule(
        "v",
        ["s1", "s2", "t1", "t2"],
        ["(s1+s2)/(t1+t2)"],
        "Ikki ketma-ket bosqich, yo‘llar o‘zaro va vaqtlar o‘zaro bir birlikda; umumiy yo‘l/umumiy vaqt; PDF50.",
    ),
    "earth_weight": rule(
        "F",
        ["m", "g"],
        ["m*g", "g*m"],
        "Yer sirtidagi og‘irlik kuchi moduli, g=9,81 N/kg masalada ochiq beriladi; PDF54.",
    ),
    "weight_mass": rule(
        "m",
        ["F", "g"],
        ["F/g", "F*g^-1"],
        "F og‘irlik kuchi, g=9,81 N/kg; massani topish; PDF54–55.",
    ),
    "pressure": rule(
        "p",
        ["F", "S"],
        ["F/S", "F*S^-1"],
        "F sirtga tik kuch, S>0 tegish yuzasi; o‘rtacha bosim; PDF57–58.",
    ),
    "pressure_force": rule(
        "F", ["p", "S"], ["p*S", "S*p"], "Bir tekis bosim p, yuza S; PDF57–59."
    ),
    "pressure_area": rule(
        "S",
        ["F", "p"],
        ["F/p", "F*p^-1"],
        "Tik kuch F, musbat bosim p; PDF59,5-mashq1.",
    ),
    "rectangle_area": rule(
        "S",
        ["a", "b"],
        ["a*b", "b*a"],
        "To‘g‘ri to‘rtburchakning musbat tomonlari bir uzunlik birligida; PDF58.",
    ),
    "hydraulic_force": rule(
        "F2",
        ["F1", "S1", "S2"],
        ["F1*S2/S1", "S2/S1*F1", "F1*(S2/S1)"],
        "Ideal gidravlik press, ishqalanish va sath farqi e’tiborsiz; S1>0, S2>0 bir yuza birligida; PDF60–61.",
    ),
    "hydrostatic": rule(
        "p",
        ["rho", "g", "h"],
        ["rho*g*h"],
        "Bir jinsli tinch suyuqlik: faqat ustun hissasi p=rho*g*h; g=9,81 N/kg, h>=0, tashqi bosim qo‘shilmagan; PDF62.",
    ),
    "communicating_height": rule(
        "h2",
        ["rho1", "h1", "rho2"],
        ["rho1*h1/rho2", "h1*(rho1/rho2)"],
        "Aralashmaydigan ikki tinch suyuqlik, ochiq sirtlarda bir xil bosim, ustunlar umumiy chegara sathidan; rho1*h1=rho2*h2; PDF63.",
    ),
    "atm_to_pa": rule(
        "y",
        ["x"],
        ["101325*x", "x*101325"],
        "x standart atmosfera birligida, y Pa; 1 atm=101325 Pa; PDF66. Har kungi bosim doim 1 atm degani emas.",
    ),
    "buoyancy": rule(
        "FA",
        ["rho", "V", "g"],
        ["rho*V*g"],
        "rho muhit zichligi; V SIQIB CHIQARILGAN suyuqlik/gaz hajmi. To‘liq botganda jism hajmi; g=9,81 N/kg; PDF68–69.",
    ),
    "buoyancy_readings": rule(
        "FA",
        ["Ph", "Ps"],
        ["Ph-Ps"],
        "Tinch osilgan jismning havo/suyuqlikdagi ko‘rsatishlari, havo ko‘tarish kuchi e’tiborsiz, Ph>=Ps; PDF68.",
    ),
    "parallel_work": rule(
        "A",
        ["F", "s"],
        ["F*s", "s*F"],
        "O‘zgarmas kuch ko‘chish bilan bir yo‘nalishda; s>=0. Perpendikulyar holat uchun F*s formulasi ishlatilmaydi; PDF71–72.",
    ),
    "work_force": rule(
        "F",
        ["A", "s"],
        ["A/s", "A*s^-1"],
        "Parallel o‘zgarmas kuch, s>0; A=F*s dan; PDF71.",
    ),
    "work_distance": rule(
        "s",
        ["A", "F"],
        ["A/F", "A*F^-1"],
        "Parallel o‘zgarmas kuch F>0; A=F*s dan; PDF71.",
    ),
    "potential_energy": rule(
        "Ep",
        ["m", "g", "h"],
        ["m*g*h"],
        "Yer sirti yaqinida tanlangan nol sathga nisbatan h>=0; g=9,81 N/kg berilgan; PDF73.",
    ),
    "kinetic_energy": rule(
        "Ek",
        ["m", "v"],
        ["m*v^2/2", "m*v*v/2", "0.5*m*v^2"],
        "m>0, v>=0 tezlik moduli, klassik maktab mexanikasi modeli; PDF73.",
    ),
    "power": rule(
        "N",
        ["A", "t"],
        ["A/t", "A*t^-1"],
        "N darslikdagi QUvVAT belgisi, birligi W. A ish, t>0; o‘rtacha quvvat; PDF74.",
    ),
    "power_work": rule(
        "A",
        ["N", "t"],
        ["N*t", "t*N"],
        "N shu oraliqdagi o‘rtacha yoki o‘zgarmas quvvat W da; A=N*t; PDF74–76.",
    ),
    "double_wheel_gain": rule(
        "n",
        ["R1", "r1", "R2", "r2"],
        ["(R1/r1)*(R2/r2)", "R1*R2/(r1*r2)"],
        "Darslikdagi ideal ikki bosqichli lebyodka; musbat radius/yelkalar bir birlikda; PDF92.",
    ),
    "moment": rule(
        "M",
        ["F", "l"],
        ["F*l", "l*F"],
        "l — o‘qdan kuch ta’sir chizig‘igacha tik yelka; F>=0. Moment moduli, N*m; PDF87.",
    ),
    "lever_force": rule(
        "F2",
        ["F1", "l1", "l2"],
        ["F1*l1/l2", "F1*(l1/l2)"],
        "Qarama-qarshi aylantiruvchi ikki moment, ideal muvozanat, musbat tik yelkalar bir birlikda; F1*l1=F2*l2; PDF88–90.",
    ),
    "lever_arm": rule(
        "l2",
        ["F1", "l1", "F2"],
        ["F1*l1/F2", "l1*(F1/F2)"],
        "Ideal richag muvozanati; F1,F2>0 bir birlikda; PDF88–90.",
    ),
    "movable_pulley": rule(
        "F",
        ["P"],
        ["P/2", "0.5*P"],
        "Ideal bitta ko‘char blok, ikki vertikal tayanch ip, o‘z vazni/ishqalanish e’tiborsiz; P yuk og‘irligi; PDF91.",
    ),
    "incline_force": rule(
        "F",
        ["P", "h", "s"],
        ["P*h/s", "P*(h/s)"],
        "Ideal qiya tekislik, tekis harakat; P og‘irlik kuchi, 0<h<=s; h,s bir birlikda; PDF91.",
    ),
    "wheel_force": rule(
        "F",
        ["P", "r", "R"],
        ["P*r/R", "P*(r/R)"],
        "Ideal chig‘iriq; P yuk og‘irligi, r baraban radiusi, R dastak yelkasi; r,R>0 bir birlikda; PDF91–92.",
    ),
    "ideal_travel": rule(
        "s1",
        ["F2", "s2", "F1"],
        ["F2*s2/F1", "s2*(F2/F1)"],
        "Yo‘qotishsiz ideal mexanizmda F1*s1=F2*s2, parallel kuchlar, F1>0; PDF93–94.",
    ),
    "pulley_travel": rule(
        "s",
        ["h"],
        ["2*h", "h*2"],
        "Ideal bitta ko‘char blokni h ko‘tarishda ikki tayanch ipning erkin uchi yo‘li; PDF94.",
    ),
    "efficiency": rule(
        "eta",
        ["Af", "Au"],
        ["Af/Au", "Af*Au^-1"],
        "Af foydali ish, Au>0 umumiy ish; 0<=Af<=Au. eta nisbat, javob 1 yoki % birligida; PDF95.",
    ),
    "efficiency_work": rule(
        "Af",
        ["eta", "Au"],
        ["eta*Au", "Au*eta"],
        "eta 0..1 nisbat (masalan80%=0,8), Au>0 umumiy ish; PDF95,97.",
    ),
    "incline_efficiency": rule(
        "eta",
        ["P", "h", "F", "s"],
        ["P*h/(F*s)", "(P*h)/(F*s)"],
        "Tekis ko‘tarish: foydali ish P*h, umumiy ish F*s; 0<h<=s, 0<=P*h<=F*s; PDF96.",
    ),
}
DIMENSION_UNIT = {
    "length": "m",
    "time": "s",
    "mass": "kg",
    "area": "m2",
    "volume": "m3",
    "density": "kg/m3",
    "speed": "m/s",
    "force": "N",
    "pressure": "Pa",
    "force_per_mass": "N/kg",
    "dimensionless": "1",
    "energy": "J",
    "power": "W",
    "torque": "N*m",
    "voltage": "V",
    "optical_power": "dptr",
    "frequency": "Hz",
    "acceleration": "m/s2",
    "angle": "rad",
    "angular_speed": "rad/s",
    "stiffness": "N/m",
}


def reviewed_calculation(question):
    """Exact independent arithmetic, with source/model and unit-domain checks."""
    name = question["grading_spec"]["rule"]
    givens = {g["symbol"]: g for g in question["public"]["givens"]}
    if set(givens) != set(REVIEWED_FORMULAS[name]["variables"]):
        raise ValueError("given_symbols_mismatch")

    def value(symbol, dimension):
        given = givens[symbol]
        unit = UNITS.get(given["unit"])
        amount = numeric(given["value"])
        if not unit or unit[0] != dimension or amount < 0:
            raise ValueError("given_quantity_domain")
        return amount * unit[1]

    def positive(symbol, dimension):
        result = value(symbol, dimension)
        if result <= 0:
            raise ValueError("positive_quantity_required")
        return result

    def same_units(*symbols):
        if len({givens[s]["unit"] for s in symbols}) != 1:
            raise ValueError("same_given_units_required")

    def gravity():
        result = positive("g", "force_per_mass")
        if result != Fraction(981, 100):
            raise ValueError("grade6_source_gravity_is_9_81")
        return result

    if name == "double_wheel_gain":
        same_units("R1", "r1", "R2", "r2")
        return (positive("R1", "length") / positive("r1", "length")) * (
            positive("R2", "length") / positive("r2", "length")
        ), "dimensionless"
    if name == "moment":
        return value("F", "force") * value("l", "length"), "torque"
    if name == "lever_force":
        same_units("l1", "l2")
        return positive("F1", "force") * positive("l1", "length") / positive(
            "l2", "length"
        ), "force"
    if name == "lever_arm":
        same_units("F1", "F2")
        return positive("F1", "force") * positive("l1", "length") / positive(
            "F2", "force"
        ), "length"
    if name == "movable_pulley":
        return positive("P", "force") / 2, "force"
    if name in {"incline_force", "wheel_force"}:
        a, b = ("h", "s") if name == "incline_force" else ("r", "R")
        same_units(a, b)
        numerator, denominator = positive(a, "length"), positive(b, "length")
        if name == "incline_force" and numerator > denominator:
            raise ValueError("incline_height_exceeds_length")
        return positive("P", "force") * numerator / denominator, "force"
    if name == "ideal_travel":
        same_units("F1", "F2")
        return positive("F2", "force") * value("s2", "length") / positive(
            "F1", "force"
        ), "length"
    if name == "pulley_travel":
        return 2 * value("h", "length"), "length"
    if name == "efficiency":
        same_units("Af", "Au")
        fraction = value("Af", "energy") / positive("Au", "energy")
        if fraction > 1:
            raise ValueError("efficiency_exceeds_one")
        return fraction, "dimensionless"
    if name == "efficiency_work":
        fraction = value("eta", "dimensionless")
        if fraction > 1:
            raise ValueError("efficiency_exceeds_one")
        return fraction * positive("Au", "energy"), "energy"
    if name == "incline_efficiency":
        same_units("h", "s")
        height, length = positive("h", "length"), positive("s", "length")
        fraction = positive("P", "force") * height / (positive("F", "force") * length)
        if height > length or fraction > 1:
            raise ValueError("invalid_incline_efficiency_domain")
        return fraction, "dimensionless"

    if name == "hydrostatic":
        return positive("rho", "density") * gravity() * value("h", "length"), "pressure"
    if name == "communicating_height":
        same_units("rho1", "rho2")
        return positive("rho1", "density") * positive("h1", "length") / positive(
            "rho2", "density"
        ), "length"
    if name == "atm_to_pa":
        if givens["x"]["unit"] != "atm":
            raise ValueError("conversion_given_unit")
        return value("x", "pressure"), "pressure"
    if name == "buoyancy":
        return positive("rho", "density") * positive("V", "volume") * gravity(), "force"
    if name == "buoyancy_readings":
        same_units("Ph", "Ps")
        result = positive("Ph", "force") - value("Ps", "force")
        if result < 0:
            raise ValueError("negative_buoyancy_readings")
        return result, "force"
    if name == "parallel_work":
        return value("F", "force") * value("s", "length"), "energy"
    if name == "work_force":
        return value("A", "energy") / positive("s", "length"), "force"
    if name == "work_distance":
        return value("A", "energy") / positive("F", "force"), "length"
    if name == "potential_energy":
        return positive("m", "mass") * gravity() * value("h", "length"), "energy"
    if name == "kinetic_energy":
        return positive("m", "mass") * value("v", "speed") ** 2 / 2, "energy"
    if name == "power":
        return value("A", "energy") / positive("t", "time"), "power"
    if name == "power_work":
        return value("N", "power") * value("t", "time"), "energy"

    if name in {"km_to_m", "min_to_s", "hour_to_s"}:
        unit, dimension = {
            "km_to_m": ("km", "length"),
            "min_to_s": ("min", "time"),
            "hour_to_s": ("h", "time"),
        }[name]
        if givens["x"]["unit"] != unit:
            raise ValueError("conversion_given_unit")
        return value("x", dimension), dimension
    if name == "step_distance":
        steps = positive("n", "dimensionless")
        if steps.denominator != 1:
            raise ValueError("integer_step_count_required")
        return positive("l", "length") * steps, "length"
    if name == "motion_speed":
        return value("s", "length") / positive("t", "time"), "speed"
    if name == "motion_distance":
        return value("v", "speed") * value("t", "time"), "length"
    if name == "motion_time":
        return value("s", "length") / positive("v", "speed"), "time"
    if name == "two_stage_speed":
        same_units("s1", "s2")
        same_units("t1", "t2")
        distance = value("s1", "length") + value("s2", "length")
        duration = positive("t1", "time") + positive("t2", "time")
        return distance / duration, "speed"
    if name in {"earth_weight", "weight_mass"}:
        gravity = positive("g", "force_per_mass")
        if gravity != Fraction(981, 100):
            raise ValueError("grade6_source_gravity_is_9_81")
        if name == "earth_weight":
            return positive("m", "mass") * gravity, "force"
        return positive("F", "force") / gravity, "mass"
    if name == "pressure":
        return value("F", "force") / positive("S", "area"), "pressure"
    if name == "pressure_force":
        return value("p", "pressure") * positive("S", "area"), "force"
    if name == "pressure_area":
        return positive("F", "force") / positive("p", "pressure"), "area"
    if name == "rectangle_area":
        same_units("a", "b")
        return positive("a", "length") * positive("b", "length"), "area"
    if name == "hydraulic_force":
        same_units("S1", "S2")
        return value("F1", "force") * positive("S2", "area") / positive(
            "S1", "area"
        ), "force"

    if name == "accelerated_path":
        given = givens["a"]
        unit = UNITS.get(given["unit"])
        if not unit or unit[0] != "acceleration":
            raise ValueError("acceleration_given_unit")
        a = numeric(given["value"]) * unit[1]
        v0, t = value("v0", "speed"), value("t", "time")
        if v0 + a * t < 0:
            raise ValueError("before_stop_velocity_domain")
        return v0 * t + a * t * t / 2, "length"
    if name == "lab_acceleration":
        return 2 * positive("s", "length") / positive("t", "time") ** 2, "acceleration"
    if name == "mean_acceleration3":
        return sum(
            (positive(k, "acceleration") for k in ("a1", "a2", "a3")), Fraction()
        ) / 3, "acceleration"
    if name in {
        "fall_velocity",
        "fall_height",
        "up_velocity",
        "up_height",
        "up_peak_time",
    }:
        g = positive("g", "acceleration")
        if g not in {
            Fraction("9.81"),
            Fraction("9.8"),
            Fraction(10),
            Fraction("9.78"),
            Fraction("9.83"),
        }:
            raise ValueError("source_gravity_model")
        v0 = value("v0", "speed")
        if name == "up_peak_time":
            if v0 <= 0:
                raise ValueError("positive_launch_velocity")
            return v0 / g, "time"
        t = value("t", "time")
        if name.startswith("up_") and (v0 <= 0 or t > 2 * v0 / g):
            raise ValueError("flight_above_launch_level")
        if name == "fall_velocity":
            return v0 + g * t, "speed"
        if name == "fall_height":
            return v0 * t + g * t * t / 2, "length"
        if name == "up_velocity":
            return v0 - g * t, "speed"
        return v0 * t - g * t * t / 2, "length"
    if name == "orbit_altitude":
        h = positive("v", "speed") ** 2 / positive("g", "acceleration") - positive(
            "R", "length"
        )
        if h < 0:
            raise ValueError("orbital_altitude_above_surface")
        return h, "length"
    if name == "static_balance":
        f, limit = value("F", "force"), value("Fmax", "force")
        if f > limit:
            raise ValueError("static_limit_exceeded")
        return f, "force"
    if name == "sliding_force":
        return value("mu", "dimensionless") * positive("N", "force"), "force"
    if name == "sliding_coefficient":
        return value("f", "force") / positive("N", "force"), "dimensionless"
    if name == "rolling_force":
        return value("c", "length") * positive("P", "force") / positive(
            "r", "length"
        ), "force"
    if name == "sliding_lab_mu":
        if value("g", "acceleration") != 10:
            raise ValueError("explicit_sliding_lab_g_is_10")
        return value("F", "force") / (positive("m", "mass") * 10), "dimensionless"
    if name == "mean_mu3":
        return sum(
            (value(k, "dimensionless") for k in ("mu1", "mu2", "mu3")), Fraction()
        ) / 3, "dimensionless"
    if name in {"gravity_pair", "altitude_gravity"}:
        constant = positive("G", "gravitation_constant")
        if constant != Fraction("6.67e-11"):
            raise ValueError("explicit_grade7_G_approximation")
        if name == "gravity_pair":
            return constant * positive("m1", "mass") * positive(
                "m2", "mass"
            ) / positive("r", "length") ** 2, "force"
        return constant * positive("M", "mass") / (
            positive("R", "length") + value("h", "length")
        ) ** 2, "acceleration"
    if name in {
        "gravity_force7",
        "gravity_mass7",
        "rest_weight",
        "apparent_up",
        "apparent_down",
        "load_factor",
        "horizontal_drop",
    }:
        g = positive("g", "acceleration")
        if g not in {Fraction("9.8"), Fraction(10)}:
            raise ValueError("explicit_grade7_near_surface_g")
        if name == "gravity_mass7":
            return positive("F", "force") / g, "mass"
        if name == "horizontal_drop":
            return g * value("t", "time") ** 2 / 2, "length"
        if name == "load_factor":
            return (g + value("a", "acceleration")) / g, "dimensionless"
        m = positive("m", "mass")
        if name in {"gravity_force7", "rest_weight"}:
            return m * g, "force"
        a = value("a", "acceleration")
        if name == "apparent_down" and a > g:
            raise ValueError("no_negative_support_force")
        return m * (g - a if name == "apparent_down" else g + a), "force"
    if name == "horizontal_range":
        return value("v0", "speed") * value("t", "time"), "length"
    if name == "orbital_radius":
        return positive("v", "speed") ** 2 / positive("g", "acceleration"), "length"
    if name == "newton_acceleration":
        return value("F", "force") / positive("m", "mass"), "acceleration"
    if name == "newton_force":
        return positive("m", "mass") * value("a", "acceleration"), "force"
    if name == "newton_mass":
        return positive("F", "force") / positive("a", "acceleration"), "mass"
    if name == "reaction_magnitude":
        return value("F1", "force"), "force"
    if name == "paired_acceleration":
        return positive("m1", "mass") * value("a1", "acceleration") / positive(
            "m2", "mass"
        ), "acceleration"
    if name == "centripetal_force":
        return positive("m", "mass") * value("v", "speed") ** 2 / positive(
            "R", "length"
        ), "force"
    if name == "spring_force":
        return positive("k", "stiffness") * value("x", "length"), "force"
    if name == "spring_stiffness":
        return positive("F", "force") / positive("x", "length"), "stiffness"
    if name == "spring_extension":
        return value("F", "force") / positive("k", "stiffness"), "length"
    if name == "rod_stiffness":
        return positive("E", "pressure") * positive("S", "area") / positive(
            "l", "length"
        ), "stiffness"
    if name == "lab_stiffness":
        if value("g", "acceleration") != 10:
            raise ValueError("grade7_spring_lab_g_is_10")
        return positive("m", "mass") * 10 / positive("x", "length"), "stiffness"
    if name == "mean_stiffness3":
        return sum(
            (positive(k, "stiffness") for k in ("k1", "k2", "k3")), Fraction()
        ) / 3, "stiffness"
    if name == "rotational_linear":
        return value("omega", "angular_speed") * positive("R", "length"), "speed"
    if name in {"rotation_period", "rotation_frequency"}:
        n = positive("n", "dimensionless")
        if givens["n"]["unit"] != "1" or n.denominator != 1:
            raise ValueError("whole_rotation_count_required")
        t = positive("t", "time")
        return (t / n, "time") if name == "rotation_period" else (n / t, "frequency")
    if name == "angular_from_period":
        if givens["p"]["unit"] != "1" or value("p", "dimensionless") != Fraction(
            "3.14"
        ):
            raise ValueError("explicit_pi_approximation_required")
        return 2 * Fraction("3.14") / positive("T", "time"), "angular_speed"
    if name == "centripetal":
        return value("v", "speed") ** 2 / positive("R", "length"), "acceleration"
    if name == "centripetal_radius":
        return positive("v", "speed") ** 2 / positive("ac", "acceleration"), "length"
    if name in {"force_sum2", "force_difference"}:
        a, b = value("F1", "force"), value("F2", "force")
        if name == "force_difference" and a < b:
            raise ValueError("resultant_direction_domain")
        return (a + b if name == "force_sum2" else a - b), "force"
    if name == "mass_sum2":
        same_units("m1", "m2")
        return value("m1", "mass") + value("m2", "mass"), "mass"
    if name == "arc_angle":
        return value("s", "length") / positive("R", "length"), "angle"
    if name == "angular_speed":
        return value("phi", "angle") / positive("t", "time"), "angular_speed"
    if name == "constant_acceleration":
        return (value("v", "speed") - value("v0", "speed")) / positive(
            "t", "time"
        ), "acceleration"
    if name == "accelerated_velocity":
        given = givens["a"]
        unit = UNITS.get(given["unit"])
        if not unit or unit[0] != "acceleration":
            raise ValueError("acceleration_given_unit")
        acceleration = numeric(given["value"]) * unit[1]
        result = value("v0", "speed") + acceleration * value("t", "time")
        if result < 0:
            raise ValueError("before_stop_velocity_domain")
        return result, "speed"
    if name == "linear_mean_speed":
        return (value("v0", "speed") + value("v", "speed")) / 2, "speed"
    if name == "codirectional_speed":
        return value("v1", "speed") + value("v2", "speed"), "speed"
    if name in {"codirectional_length", "opposed_length"}:
        a, b = value("a", "length"), value("b", "length")
        if name == "opposed_length" and a < b:
            raise ValueError("opposed_length_direction_domain")
        return (a + b if name == "codirectional_length" else a - b), "length"
    if name == "scaled_length":
        if givens["k"]["unit"] != "1":
            raise ValueError("scalar_multiplier_unit")
        return value("a", "length") * positive("k", "dimensionless"), "length"
    if name == "equal_intervals_distance":
        n = positive("n", "dimensionless")
        if givens["n"]["unit"] != "1" or n.denominator != 1:
            raise ValueError("whole_interval_count_required")
        return positive("d", "length") * n, "length"
    if name == "frequency_count":
        count = positive("n", "dimensionless")
        if givens["n"]["unit"] != "1" or count.denominator != 1:
            raise ValueError("whole_oscillation_count_required")
        return count / positive("t", "time"), "frequency"
    if name == "echo_distance":
        return positive("v", "speed") * positive("t", "time") / 2, "length"
    if name == "sound_absorption":
        incoming = positive("Ei", "energy")
        absorbed = value("Ea", "energy")
        if absorbed > incoming:
            raise ValueError("absorption_energy_domain")
        return absorbed / incoming, "dimensionless"
    if name == "flat_image_distance":
        return positive("d", "length"), "length"
    if name == "spherical_focus":
        return positive("R", "length") / 2, "length"
    if name == "concave_image":
        focal = positive("F", "length")
        distance = positive("d", "length")
        if distance <= focal:
            raise ValueError("real_concave_image_domain")
        return focal * distance / (distance - focal), "length"
    if name == "lens_power":
        return 1 / positive("F", "length"), "optical_power"
    if name == "lens_focal":
        return 1 / positive("D", "optical_power"), "length"
    if name == "v_to_mv":
        if givens["x"]["unit"] != "V":
            raise ValueError("conversion_given_unit")
        return value("x", "voltage"), "voltage"
    if name in {"kg_to_g", "g_to_kg", "tonne_to_kg"}:
        expected = {"kg_to_g": "kg", "g_to_kg": "g", "tonne_to_kg": "t"}[name]
        if givens["x"]["unit"] != expected:
            raise ValueError("conversion_given_unit")
        return value("x", "mass"), "mass"
    if name == "film_thickness":
        return positive("V", "volume") / positive("S", "area"), "length"
    if name == "front_speed":
        return value("h", "length") / positive("t", "time"), "speed"
    if name == "mass_sum3":
        same_units("m1", "m2", "m3")
        return sum((value(s, "mass") for s in ("m1", "m2", "m3")), Fraction()), "mass"
    if name == "tare_mass":
        same_units("M", "m0")
        result = value("M", "mass") - value("m0", "mass")
        if result < 0:
            raise ValueError("negative_tare_mass")
        return result, "mass"
    if name == "density":
        return positive("m", "mass") / positive("V", "volume"), "density"
    if name == "density_mass":
        return positive("rho", "density") * positive("V", "volume"), "mass"
    if name == "density_volume":
        return positive("m", "mass") / positive("rho", "density"), "volume"
    if name == "displacement":
        same_units("V2", "V1")
        result = value("V2", "volume") - value("V1", "volume")
        if result <= 0:
            raise ValueError("positive_displaced_volume_required")
        return result, "volume"
    if name == "box_volume":
        same_units("l1", "l2", "l3")
        return (
            positive("l1", "length")
            * positive("l2", "length")
            * positive("l3", "length")
        ), "volume"
    raise ValueError("unreviewed_formula_rule")
