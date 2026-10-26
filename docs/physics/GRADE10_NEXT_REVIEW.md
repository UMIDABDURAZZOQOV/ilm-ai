# Keyingi: 10-sinf §21–25 — 2026-10-26

§16–20 yozildi; testlar joriy checkpointda. Keyingi **§21,PDF72/bosma71**.
Asl17sahifa PDF72–75/79–91 nativehashlari va tasvirlari qayta o‘qildi.
Bu tayyorgarlik, §21–25 interaktiv darslari hali yaratilmagan.

- §21PDF72–75: source73 qanotning uzun yuqori yo‘li sabab havo albatta
  tezroq borishi (equal transit time) izohi to‘g‘ri universal dalil emas;
  havo zarralari bir vaqt uchrashishi shartligini kiritmang. Turbulence
  doim liftni oshiradi deb aytmang. Bosim taqsimoti/Magnus oqim yo‘nalishi
  bilan cheklangan konseptlar; manbada yo‘q liftcoefficientformulasi yo‘q.
  Torricelli v=sqrt(2*g*depth) ideal katta idish/kichik teshik/sameoutsidep/
  topvelocitynegligible/shuondagi chuqurlik, Hground−houtlet farqi.
  Source74g10/sqrt90≈9.5 misoli izchil; trueexactgridprivate kerak.
  Real oqim/dischargecoef va pressurisedDIY/weapon/bullet sinovi qo‘shmang.
- §22PDF79–82: davriy harakatning hammasi sinusoidal/garmonik emas,
  qaytaruvchi kuch va inertlikning o‘zi yetmaydi (linear F=−kx scope).
  x signed proyeksiya, A>=0modul. x=A*sin(theta),v=A*omega*cos(theta),
  a=−A*omega²*sin(theta)=−omega²*x izchil. PDF81(5.10) da cos xsin bilan
  mos emas;PDF82minusomega²x to‘g‘ri. Graphphase/initialphase aniq berilsin.
  Energiya sin²/cos² pulsatsiyalari x bilan aynan bir chastotali simple
  sinus emas. omega=2*pi/T rad/s, nu=N/t Hz farqli, pi3.14 yaqinlashuvi
  ochiq berilsin. No general trigsolver, providedsinPhase/cosPhasevalid
  data yoki aniq phasecritical point bilan finite graders rejalansin.
  PDF82A.05m,vmax.12m/s,x.03m:omega2.4,amax.288m/s²,
  a=−.1728m/s² (bosilgan−.073 noto‘g‘ri),vmodul.096m/sizchil;
  amax printedm/s emas m/s². Original givens va independent oracles.
- §23PDF82–86: source5.11 staticma=−kx0 noto‘g‘ri to‘liq balans,
  muvozanatda mg−k*x0=0, inkrement x EQUILIBRIUMdan bo‘lsa m*xddot=−kx.
  Ideal masslessspring/linear/lowdamping omega=sqrt(k/m),T=2*pi*sqrt(m/k).
  OriginalPDF84energy5.15–5.17 hammasida1/2 bor; native text buni yo‘qotgan,
  buni kitob xatosi deb yozmang. Eski spring_energy rule qayta ishlatilishi
  mumkin. Mathematicalpendulum smallangle6–8° approximate T=2*pi*sqrt(l/g),
  omega=sqrt(g/l),l pivottoCOM; allangles/masses/air uchun aniq emas.
  Restoringmg*sin tangentialcomponent, umumiy netvector deb emas.
  PDF86 lengths-sum T=sqrt(T1²+T2²)3/4→5 source izchil.
- §24PDF86–87: DIGITAL shartli l_thread+r,20/30/40count/timing data,
  T=t/N va g=4*pi²*l/T². Npositivewhole,periodvsalltime,centrelength,
  smallangle/idealapprox,pi given. Realstativ/sekundomer o‘lchovi bajarildi
  deyilmasin. Gmean/absolutedev/relativepercent jadvali bor; formula/
  printedcolumn native Ti ti textni originalrasm bilan ajratish kerak.
- §25PDF87–91: forced/damped/resonant/selfoscillation konseptlari.
  «Erkin tebranish amalda ishlatilmaydi»/«forced har qanday holatda
  so‘nmaydi»/«hamma qo‘ng‘iroq universal bir xil» claims ko‘chirilmang.
  Steadystate forcedfrequency driverga mos, transient emas. Resonance
  omegaDriver≈omega0 kichikdamping/schoolmodel; umumiy dampedpeak
  doim EXACTomega0 deb aytmang, manbada yo‘q responseformula qo‘shmang.
  Selfoscillator feedback/energysourcefinite, perpetualmotion emas.
  Source25formula yo‘q: majburan numericFRQ yasamang. Digital tasnif/
  tartiblash/grafik tavsifi orqali obyektiv topshiriqlar bo‘lsin.

Bu qaydlar expertapproval emas; yangi kontent sourcega qayta qo‘yib,
privatekeys/XP/replay/Biology406/Web/Kimyo va production saqlansin.

---
Quyida §16–20 va §11–15 oldidan yozilgan tarixiy manba qaydlari saqlandi.

# Keyingi: 10-sinf §16–20 — 2026-10-26

§11–15 yozildi; testlar joriy checkpointda. Quyidagi §16–20 tayyorgarligi
interaktiv dars tayyorligi emas. Asl17sahifa PDF54–57/60–72 native xeshlari
va tasvirlari o‘qildi. PDF=bosma+1. Keyingi **§16,PDF54/bosma53**.

- §16: tashqi impuls0 va bir o‘qdagi signed tezliklar. Inelastic commonv,
  elastic1D 3.15 tasvirlari tekshirildi. «Elastic deformatsiya umuman yo‘q»
  emas; qaytuvchi deformatsiya bilan kinetik energiya tiklanishi farqlandi.
  PDF56mashq3:6,6t/7,8m/s va200GJ mos emas,7,8km/s bilan mos. Taxminiy
  birlik almashtirib savol ko‘chirmang. PDF57mashq7 gravitywork−4J,dU+4,
  dK−4; bosilgan+4gravityworkxato. Mashq8 changeK−3J,loss3J. Signed
  momentum va energiya balanslari independent oracle bilan tekshirilsin.
- §17: netF0 umumiy rigidbodyda netmoment0 ni almashtirmaydi. Material
  nuqta/concurrentforces/translationalbalance doirasi aniq bo‘lsin. Massa
  markazi haqiqiy massa bitta nuqtada yig‘ilgan degani emas. Uch equilibrium
  turi restoring/away/zero tangentialforce bilan. PDF62 «ikki arqon o‘zaro
 60°» lekin PDF63diagram/yechim har biri VERTIKALDAN60° olib100N qiladi;
  yangi symmetricrope savolida burchak tayanchi/cosPhi aniq berilsin.
- §18: yelka o‘qdan kuch TA’SIR CHIZIG‘IGACHA tik masofa. Couple M=F*d,
  d ikki parallel chiziq oralig‘i,2F*d emas. Clockwisepositive bo‘lsa
  M=F1*l1−F2*l2; PDF64 oxirgiF2l2−F2l2 typo va oldingi ishoralar noizchil.
  PDF65 b/d diagramlarni textning2/3nomlari bilan ko‘r-ko‘rona tenglamang;
  fulcrum/effort/load joylashuvi aniq bo‘lsin. F=P/n ideal modelda yukni
  ushlab turgan IPSEGMENTLAR soni n, ko‘chmas bloklar soni emas.
- §19: kitob aynan mv²/R markazga intilma kuch haqida; M=I*beta va yangi
  inertsiya momenti mavzusi qo‘shilmasin. Centrifugal inertialforce bir
  jismdagi NewtonIII ikkinchi real jufti emas. Inertial/rotating tavsiflar
  ajratilsin. PDF67 topP geometriyasiz universal emas: ichki vertikalhalqa
  tepasida N=mv²/R−mg, tashqi convexbridge tepasida N=mg−mv²/R.
  Sonli contact savolida sirt/o‘q aniq. PDF68R=v²/g faqat N0 chegarasi;
  ichki halqa contactR<=v²/g, har qanday kontaktda tenglik emas. Chelak
  aylantirish/moto jismoniy tajribasi topshirilmasin.
- §20: statsionar/branchsiz mass continuityrho*S*v; incompressible bir xil
  rho bilan S*v const. Bernoulli same streamline/stationary/ideal/
  incompressible/no pump/loss shartida; balandlik ham rol o‘ynaydi.
  «Tezroq oqim har qanday holatda pastroq bosim» universal emas.
  PDF71F1l1−F2l2 keyingi satrplus typo, to‘g‘ri (p1−p2)*V. Final4.8
  izchil. Gazda siqiluvchanlikni istalgan tezlikda tashlab yubormang.
  Reynolds soni manbada yo‘q, sun’iy qo‘shilmang. Pistonmisol m1kg,
  S100cm²,h1m uchun rho1000,g9.8 bo‘lsa sqrt(21.56)≈4.643m/s,
  bosilgan4.9emas. Savolda rho/g berilsin, bosim tayanchi absolute/gauge
  bir xil va fizik jihatdan mumkin bo‘lsin. Pressurised DIY topshiriq yo‘q.

§16–20 JSONlari hali yo‘q. Mustaqil ekspert/nativeAndroid/prod/nashr
bajarilgan deyilmasin. Biology406/oldPhysics/progress/Web/Kimyo saqlansin.

---
Quyidagi §11–15 oldidan yozilgan tarixiy manba qaydlari saqlandi.

# 10-sinf §11–15 uchun manba qaydlari — 2026-10-26

Bu keyingi mualliflikka tayyorgarlik, interaktiv dars tayyorligi emas.
Asl butun `fizika_10_uzb.pdf` matn xeshlari katalog bilan solishtirildi;
PDF36–45 va48–53 dagi16sahifa tasvirlari o‘qildi. PDF=bosma+1.
Dars JSONlari hali yaratilmagan. Keyingi §11 PDF36/bosma35.

- §11 PDF36–38: aylana orbitadagi gravitatsiya inersial tavsifda
  markazga intilma tezlanish beradi; haqiqiy ikki kuch muvozanatda bekor
  bo‘lib tezlanish nol bo‘ldi deyilmasin. PDF37 `v²=g*(R+h)` da g aynan
  orbitadagi mahalliy g, sirt g si barcha balandlikda o‘zgarmas emas.
  `v²=gR` yaqin-sirt yaqinlashuvi.300–400km da qarshilik aynan nol/abadiy
  orbita degan da’vo bo‘lmasin.2.6 tasvirda `T=T1*sqrt((r/R)^3)`, r=R+h.
  PDF38 `h=6,6R≈42000km` deb bosilgan: bu qiymat markazdan orbital
  radiusga yaqin, yerdan balandlikka emas; balandlik r−R.24soat davrning
  o‘zi har qanday orbital yo‘nalishda Yer ustida qimirlamay turishni
  kafolatlamaydi. Geostatsionar balandlik bo‘yicha noto‘g‘ri manba sonini
  tayyor javob qilib ko‘chirmang; kerak bo‘lsa mustaqil ekspertga ajrating.
  11,2/16,7km/s ham barcha trayektoriya va boshlang‘ich nuqtaga universal
  amaliy sayohat tezliklari emas. Yangi masalalar boshqa original givens.
- §12 PDF38–41: tayanchga ta’sir P moduli va gravitatsion mg ni ajrating.
  Og‘irlik tezlik yo‘nalishiga emas, tezlanishga bog‘liq; yuqoriga ketayotgan
  lift sekinlashsa pastga tezlanishi mumkin. Erkin tushishda tayanch P=0,
  gravitatsiya va massa nol bo‘lmaydi. Kontakt modelida pastga a<=g.
  P/(mg) yuklama bilan mg/P «necha marta kamaydi» teskari nisbatini
  aralashtirmang. PDF39 vectorP=m(g−a) tasvirini modul formulasi sifatida
  ishlatishdan oldin o‘q belgilang. Sezish/medik thresholdlar universal emas.
- §13 PDF41–45: natijaviy kuch/proyeksiya. Tinch ishqalanish umumiy
  `f<=mu_s*N`, aynan har doim `f=mu*N` emas; mu_s/mu_k ajrating.
  `tan(alpha)=mu_s` chegarasi o‘zi albatta tezlanuvchan sirpanishni
  kafolatlamaydi. Harakatdagi blokda aniq berilgan mu_k ishlatilsin.
  Ideal Atwood: m2>m1>0, ip cho‘zilmas/massasiz, blokning inertsiya va
  ishqalanishi tashlangan; a=(m2−m1)*g/(m1+m2),T=2*m1*m2*g/(m1+m2).
  PDF44(2.14) dagi maxraj m1+m2. Keyingi indekslarni shu izchil tenglama bilan solishtiring.
  PDF44 mashq3 javobi `alpha=tg(alpha)` fizik ifoda emas; PDF45 mashq8
  tezlanish so‘ralib1kg deyilgan — yaroqsiz birlik, tayyor kalit emas.
- §14 PDF48–52: ish A=F*s*cos(alpha), kosinus yoki proyeksiya ishorali.
  Musbat ish kuch aynan parallel degani emas, musbat proyeksiya yetadi.
  Barcha kuchlar ishi bir xil ko‘chish bo‘yicha qo‘shiladi; PDF49 turli
  delta_s bilan chalkash additiv ifodani ko‘chirmang. Gravitatsion ish
  mg*(hStart−hEnd) signed. Mexanik E=K+U faqat konservativ almashinuvda
  yoki tashqi nokonservativ ish bo‘lmaganda saqlanadi; ishqalanishda to‘liq
  energiya saqlanishini mexanik E doimiyligi bilan tenglashtirmang.
  Qiya tekislikda doimiy tezlik, parallel tortish va kineticmu kerak;
  A_total=m*g*h*(1+mu*cot(alpha)),eta=1/(1+mu*cot(alpha)). PDF52(3.9)
  satr oxirida h tushib qolgan (o‘lcham noto‘g‘ri),3.10 da h bor.3.12
  oxirgi scalar F=m*g*(sin+mu*cos) izchil, oldingi vektorNcos satri emas.
- §15 PDF52–53: faqat shartli digital qayd, real dinamometr/taxta o‘lchovi
  bajarildi deyilmasin. A_total=F*l,A_useful=P*h,eta=P*h/(F*l),h<=l,
  positiveF/l,0<=useful<=total; percentage va fraction farqi. Bir xil mu
  va tekis tortish sharti bilan burchak ta’siri; umumiy har qanday mashinaga
  universal o‘zgarish deb aytilmasin.

Oldingi kurslar/Biology406/progress/web/Kimyo/prod o‘zgarmasin. Mustaqil fan
eksperti tasdig‘i, haqiqiy laboratoriya va nativeAndroid tekshiruvi qilinmagan.
