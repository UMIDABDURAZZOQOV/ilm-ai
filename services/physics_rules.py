"""Source-reviewed Physics formula families and independent SI arithmetic oracles.

No runtime evaluation of the submitted formula, no general CAS/equivalence
claim. Each alternative has a stated source domain. The content validator
recalculates answers from structured givens, independently of stored answers.
"""

from fractions import Fraction
from math import isqrt

from services.assessment_grading import UNITS, numeric, square_root_quantity


def rule(target, variables, equivalents, conditions, *, square_root=False):
    result = {
        "target": target,
        "variables": variables,
        "equivalents": equivalents,
        "conditions": conditions,
    }
    if square_root:
        result["allow_square_root"] = True
    return result


REVIEWED_FORMULAS = {
    "heat_cycle_rejected_heat": rule(
        "Qc",
        ["Qh", "eta"],
        ["Qh*(1-eta)", "(1-eta)*Qh"],
        "CYCLICheatengine,Qh>0,0<eta<1, Qc POSITIVE rejected magnitude;9PDF85.",
    ),
    "heat_cycle_work": rule(
        "A",
        ["Qh", "Qc"],
        ["Qh-Qc", "Qh+(-Qc)"],
        "CYCLICheatengine,DUcycle0,Qh/QcPOSITIVEreceived/rejectedmagnitudes,Qh>Qc>0,A_NET_BY>0;9PDF83–85.",
    ),
    "heat_cycle_efficiency": rule(
        "eta",
        ["Qh", "Qc"],
        ["(Qh-Qc)/Qh", "1-Qc/Qh"],
        "CYCLICheatengine,Qh>Qc>0,dimensionless0<eta<1,notpercentnumberunlessunit%;9PDF85.",
    ),
    "carnot_max_efficiency": rule(
        "eta",
        ["Th", "Tc"],
        ["(Th-Tc)/Th", "1-Tc/Th"],
        "REVERSIBLECARNOTmaximum betweenTWOreservoirs,Th>Tc>0K,notarbitraryrealengineequality;9PDF85.",
    ),
    "carnot_cycle_work": rule(
        "A",
        ["Th", "Tc", "Qh"],
        ["Qh*(Th-Tc)/Th", "Qh*(1-Tc/Th)"],
        "REVERSIBLECARNOTtworeservoirsTh>Tc>0K,Qh>0receivedmagnitude,netcyclework;9PDF86.",
    ),
    "cycle_efficiency_work_cold": rule(
        "eta",
        ["A", "Qc"],
        ["A/(A+Qc)", "1-Qc/(A+Qc)"],
        "CYCLICheatengine,A/Qc>0NETwork/rejectedheatmagnitudes,Qh=A+Qc;9PDF86.",
    ),
    "carnot_hot_temperature": rule(
        "Th",
        ["Tc", "eta"],
        ["Tc/(1-eta)", "Tc*(1-eta)^-1"],
        "REVERSIBLECARNOTtworeservoirs,Tc>0K,0<eta<1fraction,notordinaryrealengineinverse;9PDF87.",
    ),
    "cycle_work_cold_efficiency": rule(
        "A",
        ["eta", "Qc"],
        ["eta*Qc/(1-eta)", "Qc*eta/(1-eta)"],
        "CYCLICheatengine,Qc>0rejectedmagnitude,0<eta<1fraction;9PDF87.",
    ),
    "carnot_heat_temperature_ratio": rule(
        "Qh",
        ["Qc", "Th", "Tc"],
        ["Qc*Th/Tc", "Th*Qc/Tc"],
        "REVERSIBLECARNOTtworeservoirs,Qc>0rejectedmagnitude,Th>Tc>0K;9PDF87.",
    ),
    "fuel_power_efficiency": rule(
        "eta",
        ["P", "t", "m", "q"],
        ["P*t/(m*q)", "t*P/m/q"],
        "ProvidedconstantUSEFULP,completecombustionfuelm/q>0,time>0,0<P*t<m*q;9PDF89.",
    ),
    "fuel_heating_rise": rule(
        "DT",
        ["eta", "mf", "q", "mw", "c"],
        ["eta*mf*q/(mw*c)", "mf*q*eta/mw/c"],
        "SINGLEPHASEcconst,0<eta<1USEFULheatfraction,mfcompleteburning,NOphasechange,DT>0;9PDF89.",
    ),
    "fuel_travel_power": rule(
        "P",
        ["eta", "rho", "V", "q", "v", "s"],
        ["eta*rho*V*q*v/s", "rho*V*q*eta*v/s"],
        "CONSTANTspeedtravel,averageUSEFULpower,completecombustion,rho/V/q/v/s>0,0<eta<1;9PDF90.",
    ),
    "fuel_mass_power_time": rule(
        "m",
        ["P", "t", "eta", "q"],
        ["P*t/(eta*q)", "t*P/eta/q"],
        "CONSTANTUSEFULpower,completecombustionfuel,0<eta<1,q/time>0;9PDF90.",
    ),
    "fuel_energy": rule(
        "Qfuel",
        ["q", "m"],
        ["q*m", "m*q"],
        "COMPLETECOMBUSTION,q>0given/sourceapprox,QfuelRELEASEDMAGNITUDE>=0,notQ_TO_SYSTEM;9PDF65–66.",
    ),
    "fuel_mass": rule(
        "m",
        ["Qfuel", "q"],
        ["Qfuel/q", "Qfuel*q^-1"],
        "COMPLETECOMBUSTION,Qfuelreleasedmagnitude,q>0;9PDF66.",
    ),
    "fuel_specific_energy": rule(
        "q",
        ["Qfuel", "m"],
        ["Qfuel/m", "Qfuel*m^-1"],
        "COMPLETECOMBUSTION,Qfuel>0releasedmagnitude,m>0,qJ/kg;9PDF66.",
    ),
    "equal_fuel_mass": rule(
        "m2",
        ["m1", "q1", "q2"],
        ["m1*q1/q2", "q1*m1/q2"],
        "EQUALRELEASEDENERGYcompletecombustion,q1/q2given>0;9PDF66.",
    ),
    "fuel_useful_share": rule(
        "Quse",
        ["f", "q", "m"],
        ["f*q*m", "q*m*f"],
        "COMPLETECOMBUSTION,f0..1USEFULshare,restelsewhereenergyconserved;9PDF66.",
    ),
    "first_law_heat": rule(
        "Q",
        ["DU", "A"],
        ["DU+A", "A+DU"],
        "CLOSEDthermomodel,QSIGNEDTOsystem,DUSIGNED,AworkBYsystemSIGNED;9PDF67.",
    ),
    "first_law_delta": rule(
        "DU",
        ["Q", "A"],
        ["Q-A", "Q+(-A)"],
        "CLOSEDthermomodel,QSIGNEDTOsystem,AworkBYSIGNED,DU=U2-U1;9PDF67–68.",
    ),
    "first_law_work_by": rule(
        "A",
        ["Q", "DU"],
        ["Q-DU", "Q+(-DU)"],
        "CLOSEDthermomodel,AworkBYsystemSIGNED,QSIGNEDTOsystem;9PDF67–68.",
    ),
    "first_law_work_on": rule(
        "Aon",
        ["DU", "Q"],
        ["DU-Q", "DU+(-Q)"],
        "CLOSEDthermomodel,AonworkONsystemSIGNED=-A_BY,QSIGNEDTOsystem;9PDF68–69.",
    ),
    "adiabatic_work_by": rule(
        "A",
        ["DU"],
        ["-DU", "0-DU"],
        "ADIABATICclosedmodelQ0,AworkBYsystemSIGNED,DU=U2-U1;9PDF69.",
    ),
    "isochoric_heat_delta": rule(
        "DU",
        ["Q"],
        ["Q", "1*Q"],
        "ISOCHORICclosedmodelNOotherwork,Avolume0,QSIGNEDTOsystem;9PDF69.",
    ),
    "mono_isobaric_heat": rule(
        "Q",
        ["A"],
        ["5*A/2", "A*5/2"],
        "ONLYCLASSICALMONATOMICIDEALgas ISOBARICexpansion,A_BY>=0,Q_TO>0,40/60fractionNOTuniversal;9PDF70–71.",
    ),
    "mono_isochoric_heating_delta": rule(
        "DT",
        ["Q", "M", "m", "R"],
        ["2*Q*M/(3*m*R)", "2*Q*M/3/m/R"],
        "ONLYMONATOMICCLASSICALIDEALgas ISOCHORICHEATING,Q>0,DT>0,R8.31,Mmolar;9PDF71.",
    ),
    "mono_isochoric_heating_heat": rule(
        "Q",
        ["nu", "R", "DT"],
        ["3*nu*R*DT/2", "nu*R*DT*3/2"],
        "ONLYMONATOMICCLASSICALIDEALgas ISOCHORICHEATING,nu/DT>0,R8.31;9PDF71.",
    ),
    "mono_isochoric_heating_amount": rule(
        "nu",
        ["Q", "R", "DT"],
        ["2*Q/(3*R*DT)", "2*Q/3/R/DT"],
        "ONLYMONATOMICCLASSICALIDEALgas ISOCHORICHEATING,Q/DT>0,R8.31;9PDF71.",
    ),
    "hot_water_heat_magnitude": rule(
        "Qhot",
        ["c", "mh", "Th", "Tf"],
        ["c*mh*(Th-Tf)", "mh*c*(Th-Tf)"],
        "SINGLEPHASEwater,cconst>0,Th>TfKelvin,QhotRELEASEDPOSITIVEMAGNITUDE;9PDF74upper25,priorcPDF56.",
    ),
    "cold_water_heat_magnitude": rule(
        "Qcold",
        ["c", "mc", "Tf", "Tc"],
        ["c*mc*(Tf-Tc)", "mc*c*(Tf-Tc)"],
        "SINGLEPHASEwater,cconst>0,Tf>TcKelvin,QcoldRECEIVEDPOSITIVEMAGNITUDE;9PDF74upper25,priorcPDF56.",
    ),
    "heat_balance_residual": rule(
        "dQ",
        ["Qhot", "Qcold"],
        ["Qhot-Qcold", "Qhot+(-Qcold)"],
        "Qhot/coldnonnegativePROVIDEDdigitalmagnitudes,dQSIGNEDdifference,notclaimedphysicalmeasurement/energyviolation;9PDF74upper25.",
    ),
    "isobaric_gas_work": rule(
        "A",
        ["p", "V2", "V1"],
        ["p*(V2-V1)", "(V2-V1)*p"],
        "ISOBARIC pconstABSOLUTE,gas-BYworkA SIGNED,Vi>0;9PDF53–54.",
    ),
    "isobaric_amount_work": rule(
        "A",
        ["nu", "R", "T2", "T1"],
        ["nu*R*(T2-T1)", "R*nu*(T2-T1)"],
        "ISOBARIC SAMEamount/compositionIDEALgas,R8.31,TiKelvin>0,gas-BYwork SIGNED;9PDF54.",
    ),
    "isobaric_heated_mass": rule(
        "m",
        ["A", "M", "R", "DT"],
        ["A*M/(R*DT)", "M*A/R/DT"],
        "ISOBARIC HEATING idealgas,A>0,DT>0,Mmolar,R8.31;9PDF55.",
    ),
    "isobaric_signed_volume_change": rule(
        "DV",
        ["A", "p"],
        ["A/p", "A*p^-1"],
        "ISOBARIC pABSOLUTE>0,gas-BYworkA SIGNED,DV=V2-V1SIGNED not negativeabsolutevolume;9PDF53/55.",
    ),
    "sensible_heat": rule(
        "Q",
        ["m", "c", "T2", "T1"],
        ["m*c*(T2-T1)", "c*m*(T2-T1)"],
        "m/c>0,cCONSTANT,NOphasechange,TpositiveKelvin,QheatTOBODY SIGNED;9PDF56.",
    ),
    "specific_heat_from_change": rule(
        "c",
        ["Q", "m", "T2", "T1"],
        ["Q/(m*(T2-T1))", "Q/m/(T2-T1)"],
        "NOphasechange,nonzeroDT,Q SAMEsignDT,c>0;Q signedTOBODY;9PDF56.",
    ),
    "water_mix_temperature": rule(
        "Tf",
        ["mh", "Th", "mc", "Tc"],
        ["(mh*Th+mc*Tc)/(mh+mc)", "(Th*mh+Tc*mc)/(mc+mh)"],
        "TWOWATERSAMEconstantc,NOphasechange,positiveKelvinTh>Tc,m>0,negligiblevessel/externalheat/work;9PDF57–58.",
    ),
    "calorimeter_specific_heat": rule(
        "ch",
        ["mw", "cw", "mc", "cc", "Tf", "Tc", "mh", "Th"],
        ["(mw*cw+mc*cc)*(Tf-Tc)/(mh*(Th-Tf))", "(mc*cc+mw*cw)*(Tf-Tc)/mh/(Th-Tf)"],
        "COLDWATER+CALORIMETER BOTHreceiveheat =>PLUS;mh/mw/c>0,mc>=0,Tc<Tf<Th,noexternalheat/work,NOphasechange;9PDF58,CORRECTSPDF64MINUSerratum.",
    ),
    "fall_temperature_rise": rule(
        "D",
        ["g", "h", "c"],
        ["g*h/c", "h*g/c"],
        "LOSTmghALLconvertedINTOsamebodyinternalenergy,cconstNOphasechange,g9.81sourceapprox;not automaticwarmingduringfreeflight;9PDF59.",
    ),
    "mono_state_delta": rule(
        "DU",
        ["p2", "V2", "p1", "V1"],
        ["3*(p2*V2-p1*V1)/2", "(p2*V2-p1*V1)*3/2"],
        "ONLYMONATOMICCLASSICALIDEALgas SAMEamount,ABSOLUTEpressures,DU=U2-U1SIGNED;9PDF60.",
    ),
    "isobaric_work_initial_state": rule(
        "A",
        ["p", "V1", "T2", "T1"],
        ["p*V1*(T2/T1-1)", "V1*p*(T2/T1-1)"],
        "ISOBARIC SAMEideal gasamount/composition,pABSOLUTE,TiKelvin>0,gas-BYworkSIGNED;9PDF60.",
    ),
    "water_cold_volume": rule(
        "Vcold",
        ["Vtotal", "Th", "Tf", "Tc"],
        ["Vtotal*(Th-Tf)/(Th-Tc)", "(Th-Tf)*Vtotal/(Th-Tc)"],
        "TWOWATERSAMEconstantc/density,additivevolumes,Tc<Tf<Th,noexternal/vesselheat,NOphasechange;9PDF61.",
    ),
    "stopped_body_temperature": rule(
        "D",
        ["eta", "v", "c"],
        ["(1-eta)*v^2/(2*c)", "v^2*(1-eta)/2/c"],
        "STOPPEDBODY,noresidualkineticenergy,eta0..1 ENVIRONMENTshare,1-etatobody,cconstNOphasechange;NOexperiment;9PDF61.",
    ),
    "mean_specific_heat3": rule(
        "cmean",
        ["c1", "c2", "c3"],
        ["(c1+c2+c3)/3", "(c3+c1+c2)/3"],
        "ThreeprovidedconditionalSAME-MATERIALspecificheatestimates,positive,cmeanarithmeticmean,NOTrealexperimentclaim;9PDF64.",
    ),
    "calorimeter_received_heat": rule(
        "Q",
        ["mw", "cw", "mc", "cc", "Tf", "Tc"],
        ["(mw*cw+mc*cc)*(Tf-Tc)", "(mc*cc+mw*cw)*(Tf-Tc)"],
        "WATER+CALORIMETER BOTHreceiveheatPLUS,mw>0,mc>=0,positivec,Tf>TcKelvin,NOphasechange;9PDF58/64.",
    ),
    "isobaric_volume": rule(
        "V2",
        ["V1", "T2", "T1"],
        ["V1*T2/T1", "T2*V1/T1"],
        "SAME idealgas amount/composition,p const,T Kelvin>0;9PDF35.",
    ),
    "isobaric_temperature": rule(
        "T2",
        ["V2", "T1", "V1"],
        ["V2*T1/V1", "T1*V2/V1"],
        "SAMEidealgas amount/composition,pconst,TiKelvin>0;9PDF35–36.",
    ),
    "isobaric_cooling": rule(
        "Dcool",
        ["T1", "V2", "V1"],
        ["T1*(1-V2/V1)", "T1*(V1-V2)/V1"],
        "ISOBARIC COOLING,SAMEideal gas,T1>0,0<V2<V1,DcoolPOSITIVE reduction;9PDF36.",
    ),
    "isobaric_heating": rule(
        "Dheating",
        ["T1", "V2", "V1"],
        ["T1*(V2-V1)/V1", "T1*(V2/V1-1)"],
        "ISOBARIC HEATING,SAMEideal gas,T1>0,V2>V1>0,DheatingPOSITIVE increase;9PDF36.",
    ),
    "isochoric_pressure": rule(
        "p2",
        ["p1", "T2", "T1"],
        ["p1*T2/T1", "T2*p1/T1"],
        "SAMEideal gasamount/composition,Vconst,ABSOLUTEp,TiKelvin>0;9PDF37.",
    ),
    "isochoric_temperature": rule(
        "T2",
        ["p2", "T1", "p1"],
        ["p2*T1/p1", "T1*p2/p1"],
        "SAMEideal gasamount/composition,Vconst,ABSOLUTEp,TiKelvin>0;9PDF37.",
    ),
    "isochoric_initial_pressure": rule(
        "p1",
        ["dp", "T1", "T2"],
        ["dp*T1/(T2-T1)", "T1*dp/(T2-T1)"],
        "SAMEideal gas,Vconst,dp>0INCREASE,T2>T1>0Kelvin,p1ABSOLUTE;9PDF38.",
    ),
    "layer_effective_thickness": rule(
        "d",
        ["V", "S"],
        ["V/S", "V*S^-1"],
        "V/S EFFECTIVE modelthickness;not exactpea/molecule diameter,packing/modeluncertainty;9PDF39.",
    ),
    "row_particle_mean": rule(
        "d",
        ["L", "N"],
        ["L/N", "L*N^-1"],
        "Average ROWmodel,L>0,NpositiveWHOLE count inunit1;9PDF39.",
    ),
    "room_volume": rule(
        "V",
        ["a", "b", "c"],
        ["a*b*c", "c*b*a"],
        "RectangularROOMmodel,positiveorthogonaledges;conditionaldigitaldata;9PDF39.",
    ),
    "room_air_density": rule(
        "rho",
        ["p", "M", "R", "T"],
        ["p*M/(R*T)", "M*p/R/T"],
        "IDEALairmodel,M29g/molsourceapprox,R8.31,TKelvin>0,pABSOLUTE;9PDF39–40.",
    ),
    "room_particle_count": rule(
        "N",
        ["n", "V"],
        ["n*V", "V*n"],
        "nNUMBERdensity,V>0,Nwholeconditionaldigitalcount;9PDF40.",
    ),
    "leaking_fixed_volume_pressure": rule(
        "p2",
        ["f", "p1", "T2", "T1"],
        ["f*p1*T2/T1", "p1*f*T2/T1"],
        "SAMEcompositionIDEALgas,Vconst,fREMAININGamountfraction0..1,TiKelvin>0,pABSOLUTE;9PDF42.",
    ),
    "isobaric_density_temperature": rule(
        "T2",
        ["rho1", "T1", "rho2"],
        ["rho1*T1/rho2", "T1*rho1/rho2"],
        "SAMEideal gascomposition,pconst,positive densities,TKelvin>0;9PDF41.",
    ),
    "isochoric_fraction_temperature": rule(
        "T1",
        ["DT", "f"],
        ["DT/f", "DT*f^-1"],
        "SAMEideal gasVconst,DTpositiveINCREASE,f=dp/p1positivefractionalpressureINCREASE;9PDF41.",
    ),
    "bubble_expansion_ratio": rule(
        "x",
        ["rho", "g", "h", "p0"],
        ["1+rho*g*h/p0", "rho*g*h/p0+1"],
        "ISOTHERMALconstantgasamountbubble,p0ABSOLUTE>0,g10N/kgsourceapprox,neglectsurfacetension/dissolution;h>=0;9PDF41.",
    ),
    "bubble_depth_ratio": rule(
        "h",
        ["x", "p0", "rho", "g"],
        ["(x-1)*p0/(rho*g)", "p0*(x-1)/rho/g"],
        "SAMEisothermalbubblemodel,x=Vsurface/Vbottom>=1,g10N/kgsourceapprox,p0ABSOLUTE;9PDF42.",
    ),
    "mono_internal_energy": rule(
        "U",
        ["nu", "R", "T"],
        ["3*nu*R*T/2", "nu*R*T*3/2"],
        "ONLYCLASSICALMONATOMICIDEALgas,nu>0,R8.31,TKelvin>=0;9PDF51.",
    ),
    "mono_delta_energy": rule(
        "DU",
        ["nu", "R", "T2", "T1"],
        ["3*nu*R*(T2-T1)/2", "nu*R*(T2-T1)*3/2"],
        "ONLYMONATOMICCLASSICALIDEALgas,SAMEamount,DU=U2-U1 SIGNED,R8.31,TiKelvin>0;9PDF51–52.",
    ),
    "mono_pressure_energy": rule(
        "p",
        ["U", "V"],
        ["2*U/(3*V)", "2*U/3/V"],
        "ONLYMONATOMICCLASSICALIDEALgas,Uinternalenergy,V>0,pABSOLUTE;9PDF51–52.",
    ),
    "mono_delta_volume": rule(
        "DU",
        ["p", "V2", "V1"],
        ["3*p*(V2-V1)/2", "p*(V2-V1)*3/2"],
        "ONLYMONATOMICCLASSICALIDEALgas,SAMEamount,pconstABSOLUTE,DU=U2-U1 SIGNED;9PDF52.",
    ),
    "kelvin_from_celsius": rule(
        "T",
        ["theta"],
        ["theta+273.15", "273.15+theta"],
        "9PDF22 exact273.15 relation,not rounded273;theta°C signed>=-273.15,answerK only.",
    ),
    "boltzmann_mean_energy": rule(
        "E",
        ["k", "T"],
        ["3*k*T/2", "k*T*3/2"],
        "CLASSICALidealgas,mean TRANSLATIONAL Eperparticle,k1.38e-23J/Ksourceapprox,T Kelvin>=0;9PDF23.",
    ),
    "thermal_pressure": rule(
        "p",
        ["n", "k", "T"],
        ["n*k*T", "k*T*n"],
        "IDEALgas,p ABSOLUTE,nnumberdensity,k1.38e-23,TKelvin>0;9PDF23.",
    ),
    "thermal_concentration": rule(
        "n",
        ["p", "k", "T"],
        ["p/(k*T)", "p/k/T"],
        "IDEALgas,p ABSOLUTE,k1.38e-23,TKelvin>0;9PDF23.",
    ),
    "gas_total_translation": rule(
        "Etotal",
        ["p", "V"],
        ["3*p*V/2", "p*V*3/2"],
        "TOTALTRANSLATIONAL kinetic energy,not arbitrary internalenergy,p ABSOLUTE,V>0;9PDF24.",
    ),
    "thermal_speed_particle": rule(
        "v",
        ["k", "T", "m0"],
        ["sqrt(3*k*T/m0)", "(3*k*T/m0)^(1/2)"],
        "IDEALgas RMS,k1.38e-23,m0kg>0,TKelvin>0;privateexactradicand+explicitrounding,9PDF25.",
        square_root=True,
    ),
    "thermal_speed_molar": rule(
        "v",
        ["R", "T", "M"],
        ["sqrt(3*R*T/M)", "(3*R*T/M)^0.5"],
        "IDEALgas RMS,R8.31J/(mol*K)sourceapprox,Mkg/mol,TKelvin>0,explicitrounding;9PDF25.",
        square_root=True,
    ),
    "particle_speed_energy": rule(
        "v",
        ["E", "m0"],
        ["sqrt(2*E/m0)", "(2*E/m0)^(1/2)"],
        "E singleparticle kineticenergy,m0>0;9PDF27.",
        square_root=True,
    ),
    "gas_constant_product": rule(
        "R",
        ["k", "NA"],
        ["k*NA", "NA*k"],
        "k1.38e-23,NA6.02e23SOURCEapprox =>8.3076 before rounding8.31;9PDF25.",
    ),
    "stern_flight_speed": rule(
        "v",
        ["omega", "R", "r", "s"],
        ["omega*R*(R-r)/s", "R*(R-r)*omega/s"],
        "Shtern flightmodel,R OUTERradius,r INNERradius,R>r>0,omega rad/s>0,s>0;not automatically RMS;9PDF26–27.",
    ),
    "molar_speed_temperature": rule(
        "T",
        ["M", "v", "R"],
        ["M*v^2/(3*R)", "M*v*v/(3*R)"],
        "IDEALgas RMS,Mkg/mol,R8.31,TKelvin;9PDF25.",
    ),
    "equal_speed_temperature": rule(
        "T1",
        ["M1", "T2", "M2"],
        ["M1*T2/M2", "T2*M1/M2"],
        "Two idealgases SAME RMS,Mi>0,T2Kelvin>0;9PDF28.",
    ),
    "warming_initial_temperature": rule(
        "T1",
        ["DT", "v2", "v1"],
        ["DT/((v2/v1)^2-1)", "DT/(v2^2/v1^2-1)"],
        "SAME gas/composition,DT>0 temperatureDIFFERENCE,v2>v1>0 RMS;9PDF29.",
    ),
    "kinetic_temperature": rule(
        "T",
        ["E", "k"],
        ["2*E/(3*k)", "2*E/3/k"],
        "IDEALgas E meanTRANSLATIONALperparticle,k1.38e-23;9PDF29.",
    ),
    "ideal_pressure_amount": rule(
        "p",
        ["nu", "R", "T", "V"],
        ["nu*R*T/V", "R*T*nu/V"],
        "IDEALgas,nu mol,R8.31,TKelvin,V>0,p ABSOLUTE;9PDF30–31.",
    ),
    "ideal_volume_amount": rule(
        "V",
        ["nu", "R", "T", "p"],
        ["nu*R*T/p", "T*R*nu/p"],
        "IDEALgas,nu mol,R8.31,TKelvin,p ABSOLUTE>0;9PDF30–31.",
    ),
    "ideal_amount_state": rule(
        "nu",
        ["p", "V", "R", "T"],
        ["p*V/(R*T)", "p*V/R/T"],
        "IDEALgas,p ABSOLUTE,R8.31,TKelvin>0;9PDF30–31.",
    ),
    "ideal_mass_state": rule(
        "m",
        ["p", "V", "M", "R", "T"],
        ["p*V*M/(R*T)", "M*p*V/R/T"],
        "IDEALgas,Mkg/mol,p ABSOLUTE,R8.31,TKelvin>0;9PDF32.",
    ),
    "combined_state_pressure": rule(
        "p2",
        ["p1", "V1", "T2", "T1", "V2"],
        ["p1*V1*T2/(T1*V2)", "p1*V1*T2/T1/V2"],
        "IDEALgas SAMEamount/composition,pABSOLUTE,TKelvin>0,no leaks;9PDF31.",
    ),
    "isothermal_volume": rule(
        "V2",
        ["p1", "V1", "p2"],
        ["p1*V1/p2", "V1*p1/p2"],
        "IDEALgas SAMEamount/composition,Tconst,pABSOLUTE>0;9PDF33–34.",
    ),
    "isothermal_pressure": rule(
        "p2",
        ["p1", "V1", "V2"],
        ["p1*V1/V2", "V1*p1/V2"],
        "IDEALgas SAMEamount/composition,Tconst,pABSOLUTE>0,V2>0;9PDF33–34.",
    ),
    "isothermal_density": rule(
        "rho2",
        ["rho1", "p2", "p1"],
        ["rho1*p2/p1", "p2*rho1/p1"],
        "IDEALgas SAMEcomposition,Tconst,pABSOLUTE>0;9PDF34.",
    ),
    "isothermal_initial_pressure": rule(
        "p1",
        ["dp", "V2", "V1"],
        ["dp*V2/(V1-V2)", "V2*dp/(V1-V2)"],
        "ISOTHERMALcompression SAMEgas,V1>V2>0,dp>0 pressureINCREASE;9PDF35.",
    ),
    "isothermal_volume_increase": rule(
        "V2",
        ["p1", "V1", "dp"],
        ["p1*V1/(p1+dp)", "V1*p1/(p1+dp)"],
        "ISOTHERMAL SAMEgas,Tconst,dp>=0 pressureINCREASE,p1ABSOLUTE>0;9PDF34.",
    ),
    "molecular_layer": rule(
        "d",
        ["V", "S"],
        ["V/S", "V*S^-1"],
        "Bir tekis BIR MOLEKULYAR qatlam farazi,d faqat modelbahosi,V/S>0;9PDF8.",
    ),
    "relative_particle_mass": rule(
        "Mr",
        ["m0", "u"],
        ["m0/u", "m0*u^-1"],
        "Mr o‘lchamsiz,u=1.66e-27kg manba yaqinlashuvi;9PDF10–11.",
    ),
    "particle_mass_relative": rule(
        "m0",
        ["Mr", "u"],
        ["Mr*u", "u*Mr"],
        "Mr>0 o‘lchamsiz,u=1.66e-27kg yaqinlashuv;9PDF10–11.",
    ),
    "particle_count_mass": rule(
        "N", ["m", "m0"], ["m/m0", "m*m0^-1"], "Bir xil zarralar,m0>0,Nbutun;9PDF11."
    ),
    "particle_count_density": rule(
        "N",
        ["rho", "V", "m0"],
        ["rho*V/m0", "V*rho/m0"],
        "Bir jinsli modda,berilgan m0>0,Nbutun;9PDF11.",
    ),
    "amount_from_count": rule(
        "nu",
        ["N", "NA"],
        ["N/NA", "N*NA^-1"],
        "Nbutun,nu modda miqdori mol,NA ochiq manbayaqinlashuvi;9PDF12.",
    ),
    "count_from_amount": rule(
        "N",
        ["nu", "NA"],
        ["nu*NA", "NA*nu"],
        "nu mol,NA1/mol berilgan yaqinlashuv,Nbutun;9PDF12.",
    ),
    "amount_from_mass": rule(
        "nu", ["m", "M"], ["m/M", "m*M^-1"], "M MOLYARkg/mol>0,mkg;nu mol;9PDF14."
    ),
    "mass_from_amount": rule(
        "m", ["nu", "M"], ["nu*M", "M*nu"], "nu mol,Mkg/mol>0;9PDF13–14."
    ),
    "molar_from_particle": rule(
        "M",
        ["m0", "NA"],
        ["m0*NA", "NA*m0"],
        "m0kg>0,NA1/mol berilgan yaqinlashuv;9PDF13.",
    ),
    "particle_from_molar": rule(
        "m0",
        ["M", "NA"],
        ["M/NA", "M*NA^-1"],
        "Mkg/mol>0,NA1/mol berilgan yaqinlashuv;9PDF13.",
    ),
    "number_concentration": rule(
        "n",
        ["N", "V"],
        ["N/V", "N*V^-1"],
        "n son konsentratsiyasi1/m3,Nbutun,V>0;9PDF14.",
    ),
    "density_from_particles": rule(
        "rho",
        ["n", "m0"],
        ["n*m0", "m0*n"],
        "n SON konsentratsiyasi1/m3,m0kg>0;9PDF14.",
    ),
    "particle_count_rod": rule(
        "N",
        ["rho", "S", "l", "m0"],
        ["rho*S*l/m0", "S*l*rho/m0"],
        "Bir jinsli sterjen,Skesim,luzunlik,m0>0,Nbutun;9PDF16.",
    ),
    "concentration_mass": rule(
        "n",
        ["m", "NA", "M", "V"],
        ["m*NA/(M*V)", "m*NA/M/V"],
        "n SONkonsentratsiyasi,Mkg/mol,V>0,NA explicit;9PDF16.",
    ),
    "coating_particle_count": rule(
        "N",
        ["rho", "S", "h", "NA", "M"],
        ["rho*S*h*NA/M", "S*h*rho*NA/M"],
        "S JAMI qoplangan yuza,yupqa tekis qatlam,chetlar e’tiborsiz,M>0,Nbutun;9PDF16.",
    ),
    "plate_area_amount": rule(
        "S",
        ["nu", "M", "rho", "h"],
        ["nu*M/(rho*h)", "nu*M/rho/h"],
        "Bir jinsli tekis plastinka,h/rho>0,nu mol;9PDF17.",
    ),
    "image_particle_size": rule(
        "d",
        ["D", "k"],
        ["D/k", "D*k^-1"],
        "D rasm diametri,k>0 birliksiz kattalashtirish,haqiqiy d;9PDF17.",
    ),
    "gas_pressure_density": rule(
        "p",
        ["rho", "v"],
        ["rho*v^2/3", "v^2*rho/3"],
        "IDEALgaz,rho>0,v RMS tezlikmoduli;9PDF19.",
    ),
    "gas_rms_speed": rule(
        "v",
        ["p", "rho"],
        ["sqrt(3*p/rho)", "(3*p/rho)^0.5", "(3*p/rho)^(1/2)"],
        "IDEALgaz,rho>0,aniq RATSIONALILDIZ,v RMS,umumiy irrationalrounding yo‘q;9PDF19.",
        square_root=True,
    ),
    "gas_pressure_particles": rule(
        "p",
        ["n", "m0", "v"],
        ["n*m0*v^2/3", "m0*n*v^2/3"],
        "IDEALgaz,n sonkonsentratsiyasi,m0>0,v RMS;9PDF19.",
    ),
    "gas_pressure_energy": rule(
        "p",
        ["n", "E"],
        ["2*n*E/3", "n*E*2/3"],
        "IDEALgaz,E bitta molekulaning O‘RTACHA ilgarilanma kinetik energiyasi;9PDF19.",
    ),
    "gas_mean_energy": rule(
        "E",
        ["p", "n"],
        ["3*p/(2*n)", "3*p/2/n"],
        "IDEALgaz,n>0,E bitta molekulaning o‘rtacha kinetik energiyasi;9PDF20.",
    ),
    "gas_density_speed": rule(
        "rho",
        ["p", "v"],
        ["3*p/v^2", "3*p/(v*v)"],
        "IDEALgaz,v>0 RMS tezlik;9PDF19–20.",
    ),
    "lorentz_force": rule(
        "F",
        ["q", "v", "B"],
        ["q*v*B", "B*v*q"],
        "v B ga TIK,bir jinsli maydon,q=|q|>0,v>=0,B>=0;magnit kuch moduli;PDF155–156.",
    ),
    "lorentz_charge": rule(
        "q",
        ["F", "v", "B"],
        ["F/(v*B)", "F/v/B"],
        "v B ga TIK,F/v/B>0,q=|q|,ishora moduldan aniqlanmaydi;PDF165.",
    ),
    "lorentz_speed": rule(
        "v",
        ["F", "q", "B"],
        ["F/(q*B)", "F/q/B"],
        "v B ga TIK,q=|q|>0,B>0,v modul;PDF166upper27-mashq3.",
    ),
    "lorentz_induction": rule(
        "B",
        ["F", "q", "v"],
        ["F/(q*v)", "F/q/v"],
        "v B ga TIK,q=|q|>0,v>0,B modul;PDF166upper27-mashq2.",
    ),
    "ampere_force": rule(
        "F",
        ["B", "I", "l"],
        ["B*I*l", "I*l*B"],
        "Sim B ga TIK,bir jinsli maydondagi to‘g‘ri l qism,F/B/I modullari;PDF150.",
    ),
    "ampere_current": rule(
        "I", ["F", "B", "l"], ["F/(B*l)", "F/B/l"], "Sim B ga TIK,B/l>0;PDF150–151."
    ),
    "ampere_induction": rule(
        "B",
        ["F", "I", "l"],
        ["F/(I*l)", "F/I/l"],
        "Sim B ga TIK,I/l>0,B birligiT;PDF150.",
    ),
    "ampere_length": rule(
        "l",
        ["F", "B", "I"],
        ["F/(B*I)", "F/B/I"],
        "Sim B ga TIK,B/I>0,l maydon ichidagi qism;PDF150/152.",
    ),
    "ampere_charge": rule(
        "q",
        ["F", "t", "B", "l"],
        ["F*t/(B*l)", "F*t/B/l"],
        "Sim B ga TIK,doimiytok,t/B/l>0;q moduli;PDF152.",
    ),
    "ampere_force_charge": rule(
        "F",
        ["B", "q", "l", "t"],
        ["B*q*l/t", "q*B*l/t"],
        "Sim B ga TIK,doimiytok,t>0;PDF152.",
    ),
    "vacuum_current": rule(
        "I",
        ["N", "e", "t"],
        ["N*e/t", "e*N/t"],
        "N manfiy bo‘lmagan butun elektronlar soni,e1.6e-19C musbatmodul,t>0;PDF130.",
    ),
    "vacuum_count": rule(
        "N",
        ["I", "t", "e"],
        ["I*t/e", "t*I/e"],
        "Anod toki moduli,e1.6e-19C,Nbutun;PDF131exercise1.",
    ),
    "vacuum_work_count": rule(
        "N",
        ["A", "U", "e"],
        ["A/(U*e)", "A/U/e"],
        "Aelektrishmoduli,U>0,e1.6e-19C,Nbutun;PDF131exercise2.",
    ),
    "electrolysis_mass_charge": rule(
        "m",
        ["k", "q"],
        ["k*q", "q*k"],
        "Berilgan tanlangan elektrod reaksiyasi uchun k,100%current-efficiency nazariy model;PDF121.",
    ),
    "electrolysis_mass_current": rule(
        "m",
        ["k", "I", "t"],
        ["k*I*t", "I*t*k"],
        "Doimiy I,berilgan k,100%current-efficiency;PDF121.",
    ),
    "electrolysis_charge": rule(
        "q", ["m", "k"], ["m/k", "m*k^-1"], "k>0,tanlangan elektrod mahsuloti;PDF122."
    ),
    "electrolysis_current": rule(
        "I",
        ["m", "k", "t"],
        ["m/(k*t)", "m/k/t"],
        "Doimiy I,k,t>0,100%efficiency model;PDF122.",
    ),
    "electrolysis_equivalent": rule(
        "k", ["m", "I", "t"], ["m/(I*t)", "m/I/t"], "I,t>0;shartli qayddan kg/C;PDF122."
    ),
    "faraday_equivalent": rule(
        "k",
        ["M", "Z", "F"],
        ["M/(Z*F)", "M/Z/F"],
        "M MOLYAR MASSA kg/mol,Z musbat butun elektron soni,F=96500C/mol manba yaqinlashuvi;PDF123–124.",
    ),
    "faraday_mass": rule(
        "m",
        ["M", "q", "Z", "F"],
        ["M*q/(Z*F)", "M*q/Z/F"],
        "Tanlangan reaksiya uchun100%current-efficiency,Mkg/mol,F96500C/mol,Zbutun;PDF124.",
    ),
    "faraday_mole_charge": rule(
        "q",
        ["n", "Z", "F"],
        ["n*Z*F", "F*Z*n"],
        "n modda miqdori mol,Z elektronlar soni,F96500C/mol;PDF124.",
    ),
    "coating_charge": rule(
        "q",
        ["rho", "S", "h", "k"],
        ["rho*S*h/k", "S*h*rho/k"],
        "S JAMI QOPLANADIGAN yuza,yupqa tekis qatlam,chetlar e’tiborsiz,100%efficiency;PDF125.",
    ),
    "coating_power_mass": rule(
        "m",
        ["k", "P", "t", "U"],
        ["k*P*t/U", "P*t*k/U"],
        "Doimiy elektriste’molP/U,k,100%current-efficiency;PDF126.",
    ),
    "coating_thickness2": rule(
        "h",
        ["k", "I", "t", "rho", "a", "b"],
        ["k*I*t/(2*rho*a*b)", "I*t*k/(2*a*b*rho)"],
        "To‘g‘ri to‘rtburchakning AYNAN IKKI yuzi,chetlar e’tiborsiz,uniformqatlam,100%efficiency;PDF126.",
    ),
    "load_current3": rule(
        "I",
        ["P1", "P2", "P3", "U"],
        ["(P1+P2+P3)/U", "(P3+P2+P1)/U"],
        "Uch parallel doimiy yuk,berilgan iste’mol quvvatlar,umumiy U>0;PDF111.",
    ),
    "parallel_heat2": rule(
        "Q2",
        ["Q1", "R1", "R2"],
        ["Q1*R1/R2", "R1*Q1/R2"],
        "Bir xil U,t,ohmik rezistiv parallel elementlar;PDF112upper21-mashq4.",
    ),
    "series_heat2": rule(
        "Q2",
        ["Q1", "R1", "R2"],
        ["Q1*R2/R1", "R2*Q1/R1"],
        "Bir xil I,t,ohmik rezistiv ketma-ket elementlar;PDF112upper21-mashq5.",
    ),
    "electric_power": rule(
        "P", ["I", "U"], ["I*U", "U*I"], "Doimiy tok/berilgan ishlash nuqtasi;PDF90–91."
    ),
    "electric_power_current": rule(
        "I", ["P", "U"], ["P/U", "P*U^-1"], "U>0,iste’mol quvvati;PDF94."
    ),
    "electric_power_resistance": rule(
        "R", ["U", "P"], ["U^2/P", "U*U/P"], "Ohmik ishlash nuqtasi,P>0;PDF93."
    ),
    "electric_power_work": rule(
        "A", ["P", "t"], ["P*t", "t*P"], "O‘zgarmas yoki shu vaqt o‘rtacha P;PDF92."
    ),
    "parallel_power2": rule(
        "P2",
        ["P1", "R1", "R2"],
        ["P1*R1/R2", "R1*P1/R2"],
        "Bir xil U,ohmik parallel ikki element;PDF94.",
    ),
    "series_power2": rule(
        "P2",
        ["P1", "R1", "R2"],
        ["P1*R2/R1", "R2*P1/R1"],
        "Bir xil I,ohmik ketma-ket ikki element;PDF95.",
    ),
    "meter_energy": rule(
        "A",
        ["W2", "W1"],
        ["W2-W1"],
        "Bir xil hisoblagichning keyingi-avvalgi sarf qaydi,aylanish/reset yo‘q;PDF92,95.",
    ),
    "mean_power3": rule(
        "Pavg",
        ["P1", "P2", "P3"],
        ["(P1+P2+P3)/3", "(P3+P2+P1)/3"],
        "Uch shartli/mavjud qayd arifmetik o‘rtachasi;PDF96 minus xatosi tuzatilgan.",
    ),
    "joule_heat": rule(
        "Q",
        ["I", "R", "t"],
        ["I^2*R*t", "I*I*R*t"],
        "Doimiy I,R,rezistiv qizish;harorat oshishini issiqlik miqdoriga tenglashtirma;PDF97.",
    ),
    "joule_heat_voltage": rule(
        "Q",
        ["U", "t", "R"],
        ["U^2*t/R", "U*U*t/R"],
        "Doimiy U,R,ohmik rezistiv model;PDF97,100.",
    ),
    "electric_efficiency": rule(
        "eta",
        ["Af", "At"],
        ["Af/At", "Af*At^-1"],
        "0<=Af<=At,At>0;eta nisbat yoki%;PDF98.",
    ),
    "electric_efficiency_power": rule(
        "eta",
        ["Pf", "Pt"],
        ["Pf/Pt", "Pf*Pt^-1"],
        "0<=Pf<=Pt,Pt>0,foydali/iste’mol quvvat;PDF99.",
    ),
    "motor_useful_work": rule(
        "Af",
        ["eta", "U", "I", "t"],
        ["eta*U*I*t", "U*I*t*eta"],
        "Doimiy U,I,t,0<=eta<=1;PDF100.",
    ),
    "power_energy_ratio": rule(
        "ratio",
        ["P1", "P2"],
        ["P1/P2", "P1*P2^-1"],
        "Ikkala iste’molchi uchun bir xil t>0,o‘zgarmas quvvat;PDF100.",
    ),
    "parallel_work2": rule(
        "A2",
        ["A1", "R1", "R2"],
        ["A1*R1/R2", "R1*A1/R2"],
        "Bir xil U va bir xil vaqt,ohmik parallel;PDF101.",
    ),
    "joule_current": rule(
        "I",
        ["Q", "R", "t"],
        ["sqrt(Q/(R*t))", "(Q/(R*t))^(1/2)", "(Q/(R*t))^0.5"],
        "Tok MODULI,R,t>0;faqat exact rational square roots;PDF100exercise5.",
        square_root=True,
    ),
    "parallel_pair_current": rule(
        "I",
        ["U", "R1", "R2"],
        ["U*(R1+R2)/(R1*R2)", "U/R1+U/R2"],
        "U aynan parallel juftlik uchlarida,umumiy zanjir U bilan almashtirma;PDF77.",
    ),
    "capacitance": rule(
        "C",
        ["q", "U"],
        ["q/U", "q*U^-1"],
        "q bitta qoplama zaryadining moduli,U>0,ideal chiziqli kondensator;PDF79.",
    ),
    "capacitor_charge": rule(
        "q", ["C", "U"], ["C*U", "U*C"], "q bir qoplama moduli,C>0;PDF81,83."
    ),
    "capacitor_voltage": rule(
        "U", ["q", "C"], ["q/C", "q*C^-1"], "C>0,q bitta qoplama moduli;PDF82."
    ),
    "plate_capacitance": rule(
        "C",
        ["eps", "e0", "S", "d"],
        ["eps*e0*S/d", "e0*eps*S/d"],
        "Yassi ideal parallel qoplamalar,bir jinsli chiziqli dielektrik,chet ta’siri e’tiborsiz,e0=8.85e-12F/m,eps>=1;PDF79.",
    ),
    "cap_parallel2": rule(
        "C",
        ["C1", "C2"],
        ["C1+C2", "C2+C1"],
        "Ikki kondensator aynan ikki umumiy tugun orasida;PDF82.",
    ),
    "cap_series2": rule(
        "C",
        ["C1", "C2"],
        ["C1*C2/(C1+C2)", "1/(1/C1+1/C2)"],
        "Dastlab zaryadsiz ideal ketma-ket kondensatorlar,oraliq izolyatsiya tuguni neytral;PDF83.",
    ),
    "cap_series3": rule(
        "C",
        ["C1", "C2", "C3"],
        ["1/(1/C1+1/C2+1/C3)"],
        "Uch ideal musbat C ketma-ket,oraliq tugunlar neytral;PDF83–84.",
    ),
    "plate_gap_square": rule(
        "d",
        ["eps", "e0", "a", "C"],
        ["eps*e0*a^2/C", "e0*eps*a*a/C"],
        "Kvadrat qoplama a>0,ideal yassi model,e0=8.85e-12F/m,eps>=1;PDF84.",
    ),
    "plate_dielectric": rule(
        "eps",
        ["C", "d", "e0", "S"],
        ["C*d/(e0*S)", "C*d/e0/S"],
        "Ideal yassi model,e0=8.85e-12F/m,eps>=1,d,S>0;PDF85.",
    ),
    "cap_mixed": rule(
        "C",
        ["C1", "C2", "C3"],
        ["C1*C2/(C1+C2)+C3", "C3+1/(1/C1+1/C2)"],
        "C1,C2 ketma-ket juftligi C3 bilan parallel;aniq ikki tashqi tugun;PDF85.",
    ),
    "electric_work_resistance": rule(
        "A",
        ["I", "R", "t"],
        ["I^2*R*t", "I*I*R*t"],
        "Doimiy tok/qarshilik,ohmik iste’molchi;PDF89.",
    ),
    "electric_work_voltage": rule(
        "A",
        ["U", "t", "R"],
        ["U^2*t/R", "U*U*t/R"],
        "Doimiy U/qarshilik,ohmik iste’molchi,R>0;PDF89.",
    ),
    "series_resistance2": rule(
        "R",
        ["R1", "R2"],
        ["R1+R2", "R2+R1"],
        "Ikki musbat rezistor ketma-ket,ideal simlar;PDF65.",
    ),
    "series_resistance3": rule(
        "R",
        ["R1", "R2", "R3"],
        ["R1+R2+R3", "R3+R2+R1"],
        "Uch musbat rezistor ketma-ket;PDF65–66.",
    ),
    "series_voltage2": rule(
        "U",
        ["U1", "U2"],
        ["U1+U2", "U2+U1"],
        "Ketma-ket ikki iste’molchi kuchlanish tushuvlari;PDF65.",
    ),
    "series_current2": rule(
        "I",
        ["U", "R1", "R2"],
        ["U/(R1+R2)", "U*(R1+R2)^-1"],
        "Ohmik ketma-ket ikki rezistor,umumiy U;PDF65–67.",
    ),
    "series_drop1": rule(
        "U1",
        ["U", "R1", "R2"],
        ["U*R1/(R1+R2)", "R1*U/(R1+R2)"],
        "Ohmik ikki ketma-ket rezistor,birinchi tushuv;PDF65–67.",
    ),
    "parallel_current2": rule(
        "I",
        ["I1", "I2"],
        ["I1+I2", "I2+I1"],
        "Bir tugunga kiruvchi/chiqishdagi ikki musbat shoxobcha miqdori;PDF68.",
    ),
    "parallel_resistance2": rule(
        "R",
        ["R1", "R2"],
        ["R1*R2/(R1+R2)", "1/(1/R1+1/R2)"],
        "Ikki rezistor bir xil ikki tugun orasida,R1,R2>0;PDF69.",
    ),
    "parallel_resistance3": rule(
        "R",
        ["R1", "R2", "R3"],
        ["1/(1/R1+1/R2+1/R3)", "R1*R2*R3/(R1*R2+R1*R3+R2*R3)"],
        "Uch musbat rezistor aynan ikki umumiy tugun orasida;PDF69.",
    ),
    "source_voltage3": rule(
        "U",
        ["U1", "U2", "U3"],
        ["U1+U2+U3", "U3+U2+U1"],
        "Mos yo‘nalishda ketma-ket3element,ideal/shartli qayd;PDF71.",
    ),
    "mixed_resistance": rule(
        "R",
        ["R1", "R2", "R3"],
        ["R1+R2*R3/(R2+R3)", "R2*R3/(R2+R3)+R1"],
        "A--R1--B va B--(R2||R3)--C,boshqa shoxobchasiz;PDF75.",
    ),
    "mixed_current": rule(
        "I",
        ["U", "R1", "R2", "R3"],
        ["U/(R1+R2*R3/(R2+R3))"],
        "U aynan A/C terminal orasida,R1 series(R2||R3);PDF75–76.",
    ),
    "ohm_current": rule(
        "I",
        ["U", "R"],
        ["U/R", "U*R^-1"],
        "Zanjir qismi,ohmik element,doimiy harorat,R>0;PDF56–58.",
    ),
    "ohm_voltage": rule(
        "U", ["I", "R"], ["I*R", "R*I"], "Ohmik element,doimiy harorat;PDF58."
    ),
    "ohm_resistance": rule(
        "R",
        ["U", "I"],
        ["U/I", "U*I^-1"],
        "I>0;R=U/I o‘lchangan nisbat,universal R∝U qonuni emas;PDF58,62.",
    ),
    "ohm_wire_current": rule(
        "I",
        ["U", "S", "rho", "l"],
        ["U*S/(rho*l)", "U*S/rho/l"],
        "Bir jinsli sim,doimiy berilgan rho/harorat,l,S>0;PDF58,60.",
    ),
    "ohm_wire_length": rule(
        "l",
        ["U", "S", "rho", "I"],
        ["U*S/(rho*I)", "U*S/rho/I"],
        "Bir jinsli sim,doimiy berilgan rho/harorat;PDF60.",
    ),
    "ohm_wire_voltage": rule(
        "U",
        ["I", "rho", "l", "S"],
        ["I*rho*l/S", "rho*l*I/S"],
        "Bir jinsli sim,doimiy berilgan rho/harorat;PDF60.",
    ),
    "ohm_charge_resistance": rule(
        "R", ["U", "t", "q"], ["U*t/q", "t*U/q"], "Doimiy tok va U,q>0,t>0,I=q/t;PDF61."
    ),
    "ohm_electron_count": rule(
        "n",
        ["U", "t", "R", "e"],
        ["U*t/(R*e)", "U*t/R/e"],
        "Ohmik element,e1.6e-19C va butun elektron soni;PDF61.",
    ),
    "mean_resistance4": rule(
        "Ravg",
        ["R1", "R2", "R3", "R4"],
        ["(R1+R2+R3+R4)/4", "(R4+R3+R2+R1)/4"],
        "To‘rt shartli yoki mavjud qayd arifmetik o‘rtachasi,haqiqiy tajriba da’vosi emas;PDF62.",
    ),
    "voltage_work": rule(
        "U", ["A", "q"], ["A/q", "A*q^-1"], "q>0 zaryad moduli,U ish/zaryad;PDF39."
    ),
    "electric_work": rule(
        "A", ["q", "U"], ["q*U", "U*q"], "Doimiy U,zaryad moduli;PDF41."
    ),
    "work_charge": rule(
        "q", ["A", "U"], ["A/U", "A*U^-1"], "U>0,ish va zaryad modullari;PDF41."
    ),
    "series_cells": rule(
        "U",
        ["n", "U0"],
        ["n*U0", "U0*n"],
        "Bir xil elementlar mos yo‘nalishda ketma-ket,ideal kuchlanishlar yig‘indisi;n butun;PDF40.",
    ),
    "current_strength": rule(
        "I", ["q", "t"], ["q/t", "q*t^-1"], "t>0 vaqt davomida q zaryad moduli;PDF42."
    ),
    "current_charge": rule("q", ["I", "t"], ["I*t", "t*I"], "Doimiy tok moduli;PDF43."),
    "current_time": rule("t", ["q", "I"], ["q/I", "q*I^-1"], "I>0 doimiy tok;PDF46."),
    "current_electron_count": rule(
        "n",
        ["I", "t", "e"],
        ["I*t/e", "t*I/e"],
        "e=1.6e-19C;butun elektronlar soni;PDF43.",
    ),
    "electric_work_current": rule(
        "A",
        ["U", "I", "t"],
        ["U*I*t", "I*t*U", "U*(I*t)"],
        "Doimiy U va I,ish moduli;PDF45.",
    ),
    "current_work_voltage": rule(
        "U", ["A", "I", "t"], ["A/(I*t)", "A/I/t"], "I,t>0;PDF46."
    ),
    "current_electron_mass": rule(
        "m",
        ["I", "t", "e", "m0"],
        ["I*t*m0/e", "m0*(I*t/e)"],
        "Butun elektronlar soni,e1.6e-19C,m0=9.1e-31kg;PDF45.",
    ),
    "wire_resistance": rule(
        "R",
        ["rho", "l", "S"],
        ["rho*l/S", "l*rho/S"],
        "Bir jinsli sim,doimiy material/harorat,l,S>0;PDF49–51.",
    ),
    "wire_resistivity": rule(
        "rho", ["R", "S", "l"], ["R*S/l", "S*R/l"], "Bir jinsli sim,l>0;PDF51."
    ),
    "wire_length": rule(
        "l", ["R", "S", "rho"], ["R*S/rho", "S*R/rho"], "Bir jinsli sim,rho>0;PDF51–52."
    ),
    "wire_area": rule(
        "S", ["rho", "l", "R"], ["rho*l/R", "l*rho/R"], "Bir jinsli sim,R>0;PDF51–52."
    ),
    "field_charge": rule(
        "q", ["F", "E"], ["F/E", "F*E^-1"], "Kuch va maydon MODULLARI,E>0;8sinfPDF25."
    ),
    "field_electron_count": rule(
        "n",
        ["F", "e", "E"],
        ["F/(e*E)", "F/e/E"],
        "Manfiy zaryaddagi ortiqcha butun elektronlar soni,e1.6e-19C;8sinfPDF25.",
    ),
    "point_dielectric_ratio": rule(
        "eps",
        ["k", "q", "E", "r"],
        ["k*q/(E*r^2)", "k*q/E/r^2"],
        "Bir jinsli elektrostatik muhit,k9e9,qmodul,eps>=1;8sinfPDF25.",
    ),
    "field_balance_charge": rule(
        "q",
        ["m", "g", "E"],
        ["m*g/E", "g*m/E"],
        "Muallaq tomchi moduli,faqat gravitatsiya/elektrkuch,g10,E>0;8sinfPDF25–26.",
    ),
    "lightning_distance": rule(
        "s",
        ["v", "t"],
        ["v*t", "t*v"],
        "Berilgan tovush v340m/s,kechikish t,lighttime negligibletaxmin;8sinfPDF28.",
    ),
    "charge_multiple": rule(
        "q",
        ["n", "e"],
        ["n*e", "e*n"],
        "e=1.6e-19C musbat modul,n butun elektron/protonlar soni;8sinfPDF11.",
    ),
    "electron_count": rule(
        "n",
        ["q", "e"],
        ["q/e", "q*e^-1"],
        "q zaryad MODULI,e=1.6e-19C; butun zarrachalar soni;8sinfPDF11,15.",
    ),
    "particle_mass_sum": rule(
        "m",
        ["n", "m0"],
        ["n*m0", "m0*n"],
        "n butun son,m0=9.1e-31kg elektron yoki1.67e-27kg protonning berilgan yaqinlashuvi;8sinfPDF11.",
    ),
    "coulomb_force": rule(
        "F",
        ["k", "q1", "q2", "r"],
        ["k*q1*q2/r^2", "k*q2*q1/(r*r)"],
        "Vakuum,qo‘zg‘almas nuqtalar,q1/q2 musbat MODULLAR,r>0,k9e9;8sinfPDF13–14.",
    ),
    "identical_charge2": rule(
        "q",
        ["q1", "q2"],
        ["(q1+q2)/2", "q1/2+q2/2"],
        "Bir xil ikki metall sharning ideal teng taqsimoti,yakkalangan umumiy zaryad,signedq;8sinfPDF12,16.",
    ),
    "equal_share_ratio": rule(
        "ratio",
        ["q1", "q2"],
        ["(q1+q2)^2/(4*q1*q2)"],
        "Musbat bir xil ishorali zaryadlar,bir xil sharlar,oldingi r ga qaytarish;8sinfPDF16.",
    ),
    "field_strength": rule(
        "E",
        ["F", "q"],
        ["F/q", "F*q^-1"],
        "Kichik musbat sinov zaryadi,modullar;8sinfPDF19–21.",
    ),
    "field_point": rule(
        "E",
        ["k", "q", "r"],
        ["k*q/r^2", "k*q/(r*r)"],
        "Vakuumdagi nuqtaviy manba,q modul,r>0,k9e9;8sinfPDF20.",
    ),
    "field_force": rule(
        "F",
        ["E", "q"],
        ["E*q", "q*E"],
        "Elektr maydon va sinov zaryadi modullaridan kuch moduli;8sinfPDF19–21.",
    ),
    "dielectric_field": rule(
        "E",
        ["E0", "eps"],
        ["E0/eps", "E0*eps^-1"],
        "Berilgan bir jinsli chiziqli elektrostatik dielektrik,eps>=1;8sinfPDF20.",
    ),
    "dielectric_ratio": rule(
        "eps",
        ["E0", "E"],
        ["E0/E", "E0*E^-1"],
        "Ayni manba va geometrik sharoit,E0>=E>0;8sinfPDF20–21.",
    ),
    "equal_coulomb_charge": rule(
        "q",
        ["F", "r", "k"],
        ["sqrt(F*r^2/k)", "(F*r^2/k)^0.5", "r*sqrt(F/k)"],
        "Teng moduldagi vakuum nuqtalari,F/r>0,k9e9; aniq ratsional ildizli berilganlar;8sinfPDF15.",
        square_root=True,
    ),
    "potential7": rule(
        "Ep",
        ["m", "g", "h"],
        ["m*g*h", "g*m*h"],
        "Tanlangan nol sathdan h>=0,berilgan doimiyg9.8/10;7sinfPDF146–148.",
    ),
    "gravity_work7": rule(
        "A",
        ["m", "g", "h1", "h2"],
        ["m*g*(h1-h2)", "m*g*h1-m*g*h2"],
        "Faqat og‘irlik kuchi ishi,doimiyg, tanlangan sathdan h1,h2>=0;7sinfPDF147.",
    ),
    "kinetic_change": rule(
        "A",
        ["m", "v1", "v2"],
        ["m*(v2^2-v1^2)/2", "m*v2^2/2-m*v1^2/2"],
        "Natijaviy kuch ishi,o‘zgarmas m,tezlik MODULLARI;7sinfPDF149–150.",
    ),
    "mechanical_total7": rule(
        "E",
        ["m", "g", "h", "v"],
        ["m*g*h+m*v^2/2", "0.5*m*v*v+m*g*h"],
        "Nuqta jism+Yer translational va gravitational energiyasi,doimiyg;7sinfPDF150–154.",
    ),
    "spring_energy": rule(
        "Ep",
        ["k", "x"],
        ["k*x^2/2", "0.5*k*x*x"],
        "Chiziqli elastik prujina,k>0,x deformatsiya moduli;7sinfPDF153.",
    ),
    "kinetic_balance": rule(
        "Ek2",
        ["Ek1", "Ep1", "Ep2"],
        ["Ek1+Ep1-Ep2", "Ep1-Ep2+Ek1"],
        "Konservativ model,no dissipative/externalwork,Ek2>=0;7sinfPDF152–154.",
    ),
    "parallel_power": rule(
        "N",
        ["F", "v"],
        ["F*v", "v*F"],
        "Harakat tomonidagi kuchning quvvati,F,v>=0;7sinfPDF157.",
    ),
    "power_force": rule(
        "F",
        ["N", "v"],
        ["N/v", "N*v^-1"],
        "Parallel tortish foydali quvvati N, v>0;7sinfPDF157–158.",
    ),
    "crane_efficiency7": rule(
        "eta",
        ["m", "g", "h", "N", "t"],
        ["m*g*h/(N*t)", "m*g*h/N/t"],
        "Af=mgh,Au=N*t,kirish N>0,t>0,eta<=1;7sinfPDF160.",
    ),
    "linear_momentum": rule(
        "p",
        ["m", "v"],
        ["m*v", "v*m"],
        "Bir o‘q bo‘yicha signedv, m>0;7sinfPDF125–127.",
    ),
    "force_impulse": rule(
        "I",
        ["F", "t"],
        ["F*t", "t*F"],
        "O‘zgarmas natijaviy kuch proyeksiyasi,t>=0;7sinfPDF124–126.",
    ),
    "momentum_change": rule(
        "dp",
        ["m", "v", "v0"],
        ["m*(v-v0)", "m*v-m*v0"],
        "O‘zgarmas massa,bir o‘qdagi signedtezliklar;7sinfPDF126–128.",
    ),
    "momentum_sum2": rule(
        "p",
        ["m1", "v1", "m2", "v2"],
        ["m1*v1+m2*v2", "v1*m1+v2*m2"],
        "Ikki jism,bir xil sanoq sistemasi va o‘q,signedv;7sinfPDF129–131.",
    ),
    "inelastic_velocity": rule(
        "v",
        ["m1", "v1", "m2", "v2"],
        ["(m1*v1+m2*v2)/(m1+m2)"],
        "Tashqi impuls0, yopishib birga harakat qiluvchi ikki jism,m1,m2>0;7sinfPDF131–132.",
    ),
    "recoil_velocity": rule(
        "v",
        ["m", "u", "M"],
        ["-m*u/M", "-(m*u)/M"],
        "Boshlang‘ich jami impuls0; ajralgan m va qolgan M, u ayni inertial frame;7sinfPDF133–135.",
    ),
    "directed_work": rule(
        "A",
        ["Fpr", "s"],
        ["Fpr*s", "s*Fpr"],
        "O‘zgarmas kuchning ko‘chish bo‘yicha signedproyeksiyasi,s>=0;7sinfPDF141–143.",
    ),
    "lifting_lab_work": rule(
        "A",
        ["F", "h"],
        ["F*h", "h*F"],
        "Tekis yuqoriga ko‘tarishdagi kuch moduli va musbat balandlik;7sinfPDF144–145.",
    ),
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
    "specific_energy": "J/kg",
    "specific_heat": "J/(kg*K)",
    "temperature": "K",
    "gas_constant": "J/(mol*K)",
    "amount": "mol",
    "molar_mass": "kg/mol",
    "number_density": "1/m3",
    "magnetic_induction": "T",
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
    "momentum": "kg*m/s",
    "charge": "C",
    "electric_field": "N/C",
    "current": "A",
    "resistance": "Ω",
    "resistivity": "Ω*m",
    "capacitance": "F",
    "electrochemical_equivalent": "kg/C",
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

    def projection(symbol, dimension):
        # Signed components only for explicitly reviewed one-axis momentum/work rules.
        given = givens[symbol]
        unit = UNITS.get(given["unit"])
        if not unit or unit[0] != dimension:
            raise ValueError("given_projection_unit")
        return numeric(given["value"]) * unit[1]

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

    def boltzmann():
        k = positive("k", "boltzmann_constant")
        if k != Fraction("1.38e-23"):
            raise ValueError("explicit_source_boltzmann_approximation")
        return k

    def gas_constant():
        r = positive("R", "gas_constant")
        if r != Fraction("8.31"):
            raise ValueError("explicit_source_gas_constant_approximation")
        return r

    if name == "kelvin_from_celsius":
        result = projection("theta", "celsius_reading") + Fraction("273.15")
        if result < 0:
            raise ValueError("below_absolute_zero")
        return result, "temperature"
    if name == "boltzmann_mean_energy":
        return 3 * boltzmann() * value("T", "temperature") / 2, "energy"
    if name == "thermal_pressure":
        return value("n", "number_density") * boltzmann() * positive(
            "T", "temperature"
        ), "pressure"
    if name == "thermal_concentration":
        return value("p", "pressure") / (
            boltzmann() * positive("T", "temperature")
        ), "number_density"
    if name == "gas_total_translation":
        return 3 * value("p", "pressure") * positive("V", "volume") / 2, "energy"
    if name == "thermal_speed_particle":
        return square_root_quantity(
            3 * boltzmann() * positive("T", "temperature") / positive("m0", "mass")
        ), "speed"
    if name == "thermal_speed_molar":
        return square_root_quantity(
            3
            * gas_constant()
            * positive("T", "temperature")
            / positive("M", "molar_mass")
        ), "speed"
    if name == "particle_speed_energy":
        return square_root_quantity(
            2 * value("E", "energy") / positive("m0", "mass")
        ), "speed"
    if name == "gas_constant_product":
        if positive("NA", "avogadro_constant") != Fraction("6.02e23"):
            raise ValueError("explicit_source_avogadro_approximation")
        return boltzmann() * positive("NA", "avogadro_constant"), "gas_constant"
    if name == "stern_flight_speed":
        outer, inner = positive("R", "length"), positive("r", "length")
        if outer <= inner:
            raise ValueError("outer_radius_exceeds_inner")
        return positive("omega", "angular_speed") * outer * (outer - inner) / positive(
            "s", "length"
        ), "speed"
    if name == "molar_speed_temperature":
        return positive("M", "molar_mass") * value("v", "speed") ** 2 / (
            3 * gas_constant()
        ), "temperature"
    if name == "equal_speed_temperature":
        return positive("M1", "molar_mass") * positive("T2", "temperature") / positive(
            "M2", "molar_mass"
        ), "temperature"
    if name == "warming_initial_temperature":
        v1, v2 = positive("v1", "speed"), positive("v2", "speed")
        if v2 <= v1:
            raise ValueError("warming_rms_speed_increase_required")
        return positive("DT", "temperature") / ((v2 / v1) ** 2 - 1), "temperature"
    if name == "kinetic_temperature":
        return 2 * value("E", "energy") / (3 * boltzmann()), "temperature"
    if name == "ideal_pressure_amount":
        return positive("nu", "amount") * gas_constant() * positive(
            "T", "temperature"
        ) / positive("V", "volume"), "pressure"
    if name == "ideal_volume_amount":
        return positive("nu", "amount") * gas_constant() * positive(
            "T", "temperature"
        ) / positive("p", "pressure"), "volume"
    if name == "ideal_amount_state":
        return positive("p", "pressure") * positive("V", "volume") / (
            gas_constant() * positive("T", "temperature")
        ), "amount"
    if name == "ideal_mass_state":
        return positive("p", "pressure") * positive("V", "volume") * positive(
            "M", "molar_mass"
        ) / (gas_constant() * positive("T", "temperature")), "mass"
    if name == "combined_state_pressure":
        return positive("p1", "pressure") * positive("V1", "volume") * positive(
            "T2", "temperature"
        ) / (positive("T1", "temperature") * positive("V2", "volume")), "pressure"
    if name == "isothermal_volume":
        return positive("p1", "pressure") * positive("V1", "volume") / positive(
            "p2", "pressure"
        ), "volume"
    if name == "isothermal_pressure":
        return positive("p1", "pressure") * positive("V1", "volume") / positive(
            "V2", "volume"
        ), "pressure"
    if name == "isothermal_density":
        return positive("rho1", "density") * positive("p2", "pressure") / positive(
            "p1", "pressure"
        ), "density"
    if name == "isothermal_initial_pressure":
        v1, v2 = positive("V1", "volume"), positive("V2", "volume")
        if v1 <= v2:
            raise ValueError("compression_volume_decrease_required")
        return positive("dp", "pressure") * v2 / (v1 - v2), "pressure"
    if name == "isothermal_volume_increase":
        p1 = positive("p1", "pressure")
        return p1 * positive("V1", "volume") / (p1 + value("dp", "pressure")), "volume"

    def avogadro():
        result = positive("NA", "avogadro_constant")
        if result not in {Fraction("6e23"), Fraction("6.02e23"), Fraction("6.022e23")}:
            raise ValueError("explicit_source_avogadro_approximation")
        return result

    def whole_count(result):
        if result < 0 or result.denominator != 1:
            raise ValueError("whole_particle_count")
        return result

    def count_given():
        if givens["N"]["unit"] != "1":
            raise ValueError("particle_count_unit_one")
        return whole_count(value("N", "dimensionless"))

    if name == "heat_cycle_rejected_heat":
        eta = positive("eta", "dimensionless")
        if eta >= 1:
            raise ValueError("heat_engine_fraction_between_zero_and_one")
        return positive("Qh", "energy") * (1 - eta), "energy"
    if name in {"heat_cycle_work", "heat_cycle_efficiency"}:
        hot, cold = positive("Qh", "energy"), positive("Qc", "energy")
        if hot <= cold:
            raise ValueError("engine_requires_positive_net_work")
        return (
            (hot - cold, "energy")
            if name == "heat_cycle_work"
            else ((hot - cold) / hot, "dimensionless")
        )
    if name in {
        "carnot_max_efficiency",
        "carnot_cycle_work",
        "carnot_heat_temperature_ratio",
    }:
        hot, cold = positive("Th", "temperature"), positive("Tc", "temperature")
        if hot <= cold:
            raise ValueError("hot_reservoir_must_be_hotter")
        eta = (hot - cold) / hot
        if name == "carnot_max_efficiency":
            return eta, "dimensionless"
        if name == "carnot_cycle_work":
            return positive("Qh", "energy") * eta, "energy"
        return positive("Qc", "energy") * hot / cold, "energy"
    if name == "cycle_efficiency_work_cold":
        work, cold = positive("A", "energy"), positive("Qc", "energy")
        return work / (work + cold), "dimensionless"
    if name in {
        "carnot_hot_temperature",
        "cycle_work_cold_efficiency",
        "fuel_heating_rise",
        "fuel_travel_power",
        "fuel_mass_power_time",
    }:
        eta = positive("eta", "dimensionless")
        if eta >= 1:
            raise ValueError("heat_engine_fraction_between_zero_and_one")
        if name == "carnot_hot_temperature":
            return positive("Tc", "temperature") / (1 - eta), "temperature"
        if name == "cycle_work_cold_efficiency":
            return eta * positive("Qc", "energy") / (1 - eta), "energy"
        if name == "fuel_heating_rise":
            return eta * positive("mf", "mass") * positive("q", "specific_energy") / (
                positive("mw", "mass") * positive("c", "specific_heat")
            ), "temperature"
        if name == "fuel_travel_power":
            return eta * positive("rho", "density") * positive(
                "V", "volume"
            ) * positive("q", "specific_energy") * positive("v", "speed") / positive(
                "s", "length"
            ), "power"
        return positive("P", "power") * positive("t", "time") / (
            eta * positive("q", "specific_energy")
        ), "mass"
    if name == "fuel_power_efficiency":
        work = positive("P", "power") * positive("t", "time")
        fuel = positive("m", "mass") * positive("q", "specific_energy")
        if work >= fuel:
            raise ValueError("heat_engine_requires_rejected_energy")
        return work / fuel, "dimensionless"
    if name == "fuel_energy":
        return positive("q", "specific_energy") * value("m", "mass"), "energy"
    if name == "fuel_mass":
        return value("Qfuel", "energy") / positive("q", "specific_energy"), "mass"
    if name == "fuel_specific_energy":
        return positive("Qfuel", "energy") / positive("m", "mass"), "specific_energy"
    if name == "equal_fuel_mass":
        return value("m1", "mass") * positive("q1", "specific_energy") / positive(
            "q2", "specific_energy"
        ), "mass"
    if name == "fuel_useful_share":
        f = value("f", "dimensionless")
        if f > 1:
            raise ValueError("useful_fraction_zero_to_one")
        return f * positive("q", "specific_energy") * value("m", "mass"), "energy"
    if name == "first_law_heat":
        return projection("DU", "energy") + projection("A", "energy"), "energy"
    if name == "first_law_delta":
        return projection("Q", "energy") - projection("A", "energy"), "energy"
    if name == "first_law_work_by":
        return projection("Q", "energy") - projection("DU", "energy"), "energy"
    if name == "first_law_work_on":
        return projection("DU", "energy") - projection("Q", "energy"), "energy"
    if name == "adiabatic_work_by":
        return -projection("DU", "energy"), "energy"
    if name == "isochoric_heat_delta":
        return projection("Q", "energy"), "energy"
    if name == "mono_isobaric_heat":
        return 5 * value("A", "energy") / 2, "energy"
    if name == "mono_isochoric_heating_delta":
        return 2 * positive("Q", "energy") * positive("M", "molar_mass") / (
            3 * positive("m", "mass") * gas_constant()
        ), "temperature"
    if name == "mono_isochoric_heating_heat":
        return 3 * positive("nu", "amount") * gas_constant() * positive(
            "DT", "temperature"
        ) / 2, "energy"
    if name == "mono_isochoric_heating_amount":
        return 2 * positive("Q", "energy") / (
            3 * gas_constant() * positive("DT", "temperature")
        ), "amount"
    if name == "hot_water_heat_magnitude":
        hot, final = positive("Th", "temperature"), positive("Tf", "temperature")
        if hot <= final:
            raise ValueError("hot_water_must_cool")
        return positive("c", "specific_heat") * positive("mh", "mass") * (
            hot - final
        ), "energy"
    if name == "cold_water_heat_magnitude":
        final, cold = positive("Tf", "temperature"), positive("Tc", "temperature")
        if final <= cold:
            raise ValueError("cold_water_must_warm")
        return positive("c", "specific_heat") * positive("mc", "mass") * (
            final - cold
        ), "energy"
    if name == "heat_balance_residual":
        return value("Qhot", "energy") - value("Qcold", "energy"), "energy"
    if name == "isobaric_gas_work":
        return positive("p", "pressure") * (
            positive("V2", "volume") - positive("V1", "volume")
        ), "energy"
    if name == "isobaric_amount_work":
        return positive("nu", "amount") * gas_constant() * (
            positive("T2", "temperature") - positive("T1", "temperature")
        ), "energy"
    if name == "isobaric_heated_mass":
        return positive("A", "energy") * positive("M", "molar_mass") / (
            gas_constant() * positive("DT", "temperature")
        ), "mass"
    if name == "isobaric_signed_volume_change":
        return projection("A", "energy") / positive("p", "pressure"), "volume"
    if name == "sensible_heat":
        return positive("m", "mass") * positive("c", "specific_heat") * (
            positive("T2", "temperature") - positive("T1", "temperature")
        ), "energy"
    if name == "specific_heat_from_change":
        delta = positive("T2", "temperature") - positive("T1", "temperature")
        heat = projection("Q", "energy")
        if delta == 0 or heat * delta <= 0:
            raise ValueError("heat_and_temperature_change_same_nonzero_sign")
        return heat / (positive("m", "mass") * delta), "specific_heat"
    if name == "water_mix_temperature":
        mh, mc = positive("mh", "mass"), positive("mc", "mass")
        hot, cold = positive("Th", "temperature"), positive("Tc", "temperature")
        if hot <= cold:
            raise ValueError("hot_temperature_exceeds_cold")
        return (mh * hot + mc * cold) / (mh + mc), "temperature"
    if name in {"calorimeter_specific_heat", "calorimeter_received_heat"}:
        cold, final = positive("Tc", "temperature"), positive("Tf", "temperature")
        if final <= cold:
            raise ValueError("cold_components_must_receive_heat")
        capacity = positive("mw", "mass") * positive("cw", "specific_heat") + value(
            "mc", "mass"
        ) * positive("cc", "specific_heat")
        heat = capacity * (final - cold)
        if name == "calorimeter_received_heat":
            return heat, "energy"
        hot = positive("Th", "temperature")
        if hot <= final:
            raise ValueError("hot_body_must_cool")
        return heat / (positive("mh", "mass") * (hot - final)), "specific_heat"
    if name == "fall_temperature_rise":
        g = positive("g", "force_per_mass")
        if g != Fraction("9.81"):
            raise ValueError("explicit_source_gravity_9_81")
        return g * value("h", "length") / positive("c", "specific_heat"), "temperature"
    if name == "mono_state_delta":
        return 3 * (
            positive("p2", "pressure") * positive("V2", "volume")
            - positive("p1", "pressure") * positive("V1", "volume")
        ) / 2, "energy"
    if name == "isobaric_work_initial_state":
        return positive("p", "pressure") * positive("V1", "volume") * (
            positive("T2", "temperature") / positive("T1", "temperature") - 1
        ), "energy"
    if name == "water_cold_volume":
        hot, final, cold = (
            positive("Th", "temperature"),
            positive("Tf", "temperature"),
            positive("Tc", "temperature"),
        )
        if not cold < final < hot:
            raise ValueError("mixture_temperature_between_inputs")
        return positive("Vtotal", "volume") * (hot - final) / (hot - cold), "volume"
    if name == "stopped_body_temperature":
        eta = value("eta", "dimensionless")
        if eta > 1:
            raise ValueError("energy_fraction_zero_to_one")
        return (1 - eta) * value("v", "speed") ** 2 / (
            2 * positive("c", "specific_heat")
        ), "temperature"
    if name == "mean_specific_heat3":
        return sum(
            (positive(k, "specific_heat") for k in ("c1", "c2", "c3")), Fraction()
        ) / 3, "specific_heat"
    if name == "isobaric_volume":
        return positive("V1", "volume") * positive("T2", "temperature") / positive(
            "T1", "temperature"
        ), "volume"
    if name == "isobaric_temperature":
        return positive("V2", "volume") * positive("T1", "temperature") / positive(
            "V1", "volume"
        ), "temperature"
    if name in {"isobaric_cooling", "isobaric_heating"}:
        v1, v2 = positive("V1", "volume"), positive("V2", "volume")
        if name == "isobaric_cooling":
            if v2 >= v1:
                raise ValueError("cooling_volume_decrease_required")
            return positive("T1", "temperature") * (1 - v2 / v1), "temperature"
        if v2 <= v1:
            raise ValueError("heating_volume_increase_required")
        return positive("T1", "temperature") * (v2 / v1 - 1), "temperature"
    if name == "isochoric_pressure":
        return positive("p1", "pressure") * positive("T2", "temperature") / positive(
            "T1", "temperature"
        ), "pressure"
    if name == "isochoric_temperature":
        return positive("p2", "pressure") * positive("T1", "temperature") / positive(
            "p1", "pressure"
        ), "temperature"
    if name == "isochoric_initial_pressure":
        t1, t2 = positive("T1", "temperature"), positive("T2", "temperature")
        if t2 <= t1:
            raise ValueError("warming_temperature_increase_required")
        return positive("dp", "pressure") * t1 / (t2 - t1), "pressure"
    if name == "layer_effective_thickness":
        return positive("V", "volume") / positive("S", "area"), "length"
    if name == "row_particle_mean":
        count = count_given()
        if count <= 0:
            raise ValueError("positive_particle_count")
        return positive("L", "length") / count, "length"
    if name == "room_volume":
        return positive("a", "length") * positive("b", "length") * positive(
            "c", "length"
        ), "volume"
    if name == "room_air_density":
        molar = positive("M", "molar_mass")
        if molar != Fraction("0.029"):
            raise ValueError("source_air_molar_mass_approximation")
        return positive("p", "pressure") * molar / (
            gas_constant() * positive("T", "temperature")
        ), "density"
    if name == "room_particle_count":
        return whole_count(
            value("n", "number_density") * positive("V", "volume")
        ), "dimensionless"
    if name == "leaking_fixed_volume_pressure":
        fraction = value("f", "dimensionless")
        if fraction > 1:
            raise ValueError("remaining_fraction_zero_to_one")
        return fraction * positive("p1", "pressure") * positive(
            "T2", "temperature"
        ) / positive("T1", "temperature"), "pressure"
    if name == "isobaric_density_temperature":
        return positive("rho1", "density") * positive("T1", "temperature") / positive(
            "rho2", "density"
        ), "temperature"
    if name == "isochoric_fraction_temperature":
        return positive("DT", "temperature") / positive(
            "f", "dimensionless"
        ), "temperature"
    if name in {"bubble_expansion_ratio", "bubble_depth_ratio"}:
        gravity = value("g", "force_per_mass")
        if gravity != 10:
            raise ValueError("explicit_source_gravity_10")
        rho, p0 = positive("rho", "density"), positive("p0", "pressure")
        if name == "bubble_expansion_ratio":
            return 1 + rho * gravity * value("h", "length") / p0, "dimensionless"
        ratio = positive("x", "dimensionless")
        if ratio < 1:
            raise ValueError("surface_to_bottom_ratio_at_least_one")
        return (ratio - 1) * p0 / (rho * gravity), "length"
    if name == "mono_internal_energy":
        return 3 * positive("nu", "amount") * gas_constant() * value(
            "T", "temperature"
        ) / 2, "energy"
    if name == "mono_delta_energy":
        return 3 * positive("nu", "amount") * gas_constant() * (
            positive("T2", "temperature") - positive("T1", "temperature")
        ) / 2, "energy"
    if name == "mono_pressure_energy":
        return 2 * value("U", "energy") / (3 * positive("V", "volume")), "pressure"
    if name == "mono_delta_volume":
        return 3 * positive("p", "pressure") * (
            positive("V2", "volume") - positive("V1", "volume")
        ) / 2, "energy"
    if name == "molecular_layer":
        return positive("V", "volume") / positive("S", "area"), "length"
    if name in {"relative_particle_mass", "particle_mass_relative"}:
        u = positive("u", "mass")
        if u != Fraction("1.66e-27"):
            raise ValueError("explicit_atomic_mass_approximation")
        return (
            (positive("m0", "mass") / u, "dimensionless")
            if name == "relative_particle_mass"
            else (positive("Mr", "dimensionless") * u, "mass")
        )
    if name == "particle_count_mass":
        return whole_count(value("m", "mass") / positive("m0", "mass")), "dimensionless"
    if name == "particle_count_density":
        return whole_count(
            positive("rho", "density") * value("V", "volume") / positive("m0", "mass")
        ), "dimensionless"
    if name == "amount_from_count":
        return count_given() / avogadro(), "amount"
    if name == "count_from_amount":
        return whole_count(value("nu", "amount") * avogadro()), "dimensionless"
    if name == "amount_from_mass":
        return value("m", "mass") / positive("M", "molar_mass"), "amount"
    if name == "mass_from_amount":
        return value("nu", "amount") * positive("M", "molar_mass"), "mass"
    if name == "molar_from_particle":
        return positive("m0", "mass") * avogadro(), "molar_mass"
    if name == "particle_from_molar":
        return positive("M", "molar_mass") / avogadro(), "mass"
    if name == "number_concentration":
        return count_given() / positive("V", "volume"), "number_density"
    if name == "density_from_particles":
        return value("n", "number_density") * positive("m0", "mass"), "density"
    if name == "particle_count_rod":
        return whole_count(
            positive("rho", "density")
            * positive("S", "area")
            * value("l", "length")
            / positive("m0", "mass")
        ), "dimensionless"
    if name == "concentration_mass":
        return value("m", "mass") * avogadro() / (
            positive("M", "molar_mass") * positive("V", "volume")
        ), "number_density"
    if name == "coating_particle_count":
        return whole_count(
            positive("rho", "density")
            * positive("S", "area")
            * value("h", "length")
            * avogadro()
            / positive("M", "molar_mass")
        ), "dimensionless"
    if name == "plate_area_amount":
        return value("nu", "amount") * positive("M", "molar_mass") / (
            positive("rho", "density") * positive("h", "length")
        ), "area"
    if name == "image_particle_size":
        if givens["k"]["unit"] != "1":
            raise ValueError("magnification_unit_one")
        return value("D", "length") / positive("k", "dimensionless"), "length"
    if name == "gas_pressure_density":
        return positive("rho", "density") * value("v", "speed") ** 2 / 3, "pressure"
    if name == "gas_rms_speed":
        squared = 3 * value("p", "pressure") / positive("rho", "density")
        a, b = isqrt(squared.numerator), isqrt(squared.denominator)
        if a * a != squared.numerator or b * b != squared.denominator:
            raise ValueError("reviewed_exact_rational_root_required")
        return Fraction(a, b), "speed"
    if name == "gas_pressure_particles":
        return value("n", "number_density") * positive("m0", "mass") * value(
            "v", "speed"
        ) ** 2 / 3, "pressure"
    if name == "gas_pressure_energy":
        return 2 * value("n", "number_density") * value("E", "energy") / 3, "pressure"
    if name == "gas_mean_energy":
        return 3 * value("p", "pressure") / (
            2 * positive("n", "number_density")
        ), "energy"
    if name == "gas_density_speed":
        return 3 * value("p", "pressure") / positive("v", "speed") ** 2, "density"
    if name == "lorentz_force":
        return positive("q", "charge") * value("v", "speed") * value(
            "B", "magnetic_induction"
        ), "force"
    if name == "lorentz_charge":
        return positive("F", "force") / (
            positive("v", "speed") * positive("B", "magnetic_induction")
        ), "charge"
    if name == "lorentz_speed":
        return value("F", "force") / (
            positive("q", "charge") * positive("B", "magnetic_induction")
        ), "speed"
    if name == "lorentz_induction":
        return value("F", "force") / (
            positive("q", "charge") * positive("v", "speed")
        ), "magnetic_induction"
    if name == "ampere_force":
        return value("B", "magnetic_induction") * value("I", "current") * value(
            "l", "length"
        ), "force"
    if name == "ampere_current":
        return value("F", "force") / (
            positive("B", "magnetic_induction") * positive("l", "length")
        ), "current"
    if name == "ampere_induction":
        return value("F", "force") / (
            positive("I", "current") * positive("l", "length")
        ), "magnetic_induction"
    if name == "ampere_length":
        return value("F", "force") / (
            positive("B", "magnetic_induction") * positive("I", "current")
        ), "length"
    if name == "ampere_charge":
        return value("F", "force") * positive("t", "time") / (
            positive("B", "magnetic_induction") * positive("l", "length")
        ), "charge"
    if name == "ampere_force_charge":
        return value("B", "magnetic_induction") * value("q", "charge") * value(
            "l", "length"
        ) / positive("t", "time"), "force"
    if name in {"vacuum_current", "vacuum_count", "vacuum_work_count"}:
        e = positive("e", "charge")
        if e != Fraction("1.6e-19"):
            raise ValueError("explicit_elementary_charge_magnitude")
        if name == "vacuum_current":
            count = value("N", "dimensionless")
            if givens["N"]["unit"] != "1" or count.denominator != 1:
                raise ValueError("whole_particle_count")
            return count * e / positive("t", "time"), "current"
        count = (
            value("I", "current") * value("t", "time") / e
            if name == "vacuum_count"
            else value("A", "energy") / (positive("U", "voltage") * e)
        )
        if count.denominator != 1:
            raise ValueError("whole_particle_count")
        return count, "dimensionless"
    if name == "electrolysis_mass_charge":
        return positive("k", "electrochemical_equivalent") * value(
            "q", "charge"
        ), "mass"
    if name == "electrolysis_mass_current":
        return positive("k", "electrochemical_equivalent") * value(
            "I", "current"
        ) * value("t", "time"), "mass"
    if name == "electrolysis_charge":
        return value("m", "mass") / positive(
            "k", "electrochemical_equivalent"
        ), "charge"
    if name == "electrolysis_current":
        return value("m", "mass") / (
            positive("k", "electrochemical_equivalent") * positive("t", "time")
        ), "current"
    if name == "electrolysis_equivalent":
        return positive("m", "mass") / (
            positive("I", "current") * positive("t", "time")
        ), "electrochemical_equivalent"
    if name in {"faraday_equivalent", "faraday_mass", "faraday_mole_charge"}:
        z = positive("Z", "dimensionless")
        if givens["Z"]["unit"] != "1" or z.denominator != 1:
            raise ValueError("positive_integer_electron_valence")
        f = positive("F", "faraday_constant")
        if f != 96500:
            raise ValueError("explicit_source_faraday_approximation")
        if name == "faraday_mole_charge":
            return value("n", "amount") * z * f, "charge"
        k = positive("M", "molar_mass") / (z * f)
        return (
            (k, "electrochemical_equivalent")
            if name == "faraday_equivalent"
            else (k * value("q", "charge"), "mass")
        )
    if name == "coating_charge":
        return positive("rho", "density") * positive("S", "area") * value(
            "h", "length"
        ) / positive("k", "electrochemical_equivalent"), "charge"
    if name == "coating_power_mass":
        return positive("k", "electrochemical_equivalent") * value(
            "P", "power"
        ) * value("t", "time") / positive("U", "voltage"), "mass"
    if name == "coating_thickness2":
        return positive("k", "electrochemical_equivalent") * value(
            "I", "current"
        ) * value("t", "time") / (
            2
            * positive("rho", "density")
            * positive("a", "length")
            * positive("b", "length")
        ), "length"
    if name == "load_current3":
        return sum(
            (value(k, "power") for k in ["P1", "P2", "P3"]), Fraction()
        ) / positive("U", "voltage"), "current"
    if name in {"parallel_heat2", "series_heat2"}:
        q = value("Q1", "energy")
        a, b = positive("R1", "resistance"), positive("R2", "resistance")
        return (q * a / b if name == "parallel_heat2" else q * b / a), "energy"
    if name == "electric_power":
        return value("I", "current") * value("U", "voltage"), "power"
    if name == "electric_power_current":
        return value("P", "power") / positive("U", "voltage"), "current"
    if name == "electric_power_resistance":
        return positive("U", "voltage") ** 2 / positive("P", "power"), "resistance"
    if name == "electric_power_work":
        return value("P", "power") * value("t", "time"), "energy"
    if name in {"parallel_power2", "series_power2"}:
        a, b = positive("R1", "resistance"), positive("R2", "resistance")
        p = value("P1", "power")
        return (p * a / b if name == "parallel_power2" else p * b / a), "power"
    if name == "meter_energy":
        previous, current = value("W1", "energy"), value("W2", "energy")
        if current < previous:
            raise ValueError("meter_reset_or_reversed_readings")
        return current - previous, "energy"
    if name == "mean_power3":
        return sum(
            (value(k, "power") for k in ["P1", "P2", "P3"]), Fraction()
        ) / 3, "power"
    if name == "joule_heat":
        return value("I", "current") ** 2 * positive("R", "resistance") * value(
            "t", "time"
        ), "energy"
    if name == "joule_heat_voltage":
        return value("U", "voltage") ** 2 * value("t", "time") / positive(
            "R", "resistance"
        ), "energy"
    if name in {"electric_efficiency", "electric_efficiency_power"}:
        dim = "energy" if name == "electric_efficiency" else "power"
        f = value("Af" if dim == "energy" else "Pf", dim)
        total = positive("At" if dim == "energy" else "Pt", dim)
        if f > total:
            raise ValueError("useful_energy_exceeds_input")
        return f / total, "dimensionless"
    if name == "motor_useful_work":
        eta = value("eta", "dimensionless")
        if eta > 1:
            raise ValueError("efficiency_range")
        return eta * value("U", "voltage") * value("I", "current") * value(
            "t", "time"
        ), "energy"
    if name == "power_energy_ratio":
        return value("P1", "power") / positive("P2", "power"), "dimensionless"
    if name == "parallel_work2":
        return value("A1", "energy") * positive("R1", "resistance") / positive(
            "R2", "resistance"
        ), "energy"
    if name == "joule_current":
        squared = value("Q", "energy") / (
            positive("R", "resistance") * positive("t", "time")
        )
        a, b = isqrt(squared.numerator), isqrt(squared.denominator)
        if a * a != squared.numerator or b * b != squared.denominator:
            raise ValueError("reviewed_exact_rational_root_required")
        return Fraction(a, b), "current"
    if name == "parallel_pair_current":
        voltage = value("U", "voltage")
        return voltage / positive("R1", "resistance") + voltage / positive(
            "R2", "resistance"
        ), "current"
    if name == "capacitance":
        return positive("q", "charge") / positive("U", "voltage"), "capacitance"
    if name == "capacitor_charge":
        return positive("C", "capacitance") * value("U", "voltage"), "charge"
    if name == "capacitor_voltage":
        return value("q", "charge") / positive("C", "capacitance"), "voltage"
    if name in {"plate_capacitance", "plate_gap_square", "plate_dielectric"}:
        e0 = positive("e0", "permittivity")
        if e0 != Fraction("8.85e-12"):
            raise ValueError("explicit_source_permittivity")
        if name == "plate_dielectric":
            eps = (
                positive("C", "capacitance")
                * positive("d", "length")
                / (e0 * positive("S", "area"))
            )
        else:
            eps = positive("eps", "dimensionless")
        if eps < 1:
            raise ValueError("static_dielectric_model")
        if name == "plate_capacitance":
            return eps * e0 * positive("S", "area") / positive(
                "d", "length"
            ), "capacitance"
        if name == "plate_gap_square":
            return eps * e0 * positive("a", "length") ** 2 / positive(
                "C", "capacitance"
            ), "length"
        return eps, "dimensionless"
    if name == "cap_parallel2":
        return positive("C1", "capacitance") + positive(
            "C2", "capacitance"
        ), "capacitance"
    if name in {"cap_series2", "cap_series3"}:
        keys = ["C1", "C2"] + (["C3"] if name == "cap_series3" else [])
        return 1 / sum(
            (1 / positive(k, "capacitance") for k in keys), Fraction()
        ), "capacitance"
    if name == "cap_mixed":
        a, b, c = (positive(k, "capacitance") for k in ["C1", "C2", "C3"])
        return 1 / (1 / a + 1 / b) + c, "capacitance"
    if name == "electric_work_resistance":
        return value("I", "current") ** 2 * positive("R", "resistance") * value(
            "t", "time"
        ), "energy"
    if name == "electric_work_voltage":
        return value("U", "voltage") ** 2 * value("t", "time") / positive(
            "R", "resistance"
        ), "energy"
    if name in {"series_resistance2", "series_resistance3"}:
        keys = ["R1", "R2"] + (["R3"] if name == "series_resistance3" else [])
        return sum((positive(k, "resistance") for k in keys), Fraction()), "resistance"
    if name == "series_voltage2":
        return value("U1", "voltage") + value("U2", "voltage"), "voltage"
    if name in {"series_current2", "series_drop1"}:
        r1, r2 = positive("R1", "resistance"), positive("R2", "resistance")
        current = value("U", "voltage") / (r1 + r2)
        return (
            (current, "current")
            if name == "series_current2"
            else (current * r1, "voltage")
        )
    if name == "parallel_current2":
        return value("I1", "current") + value("I2", "current"), "current"
    if name in {"parallel_resistance2", "parallel_resistance3"}:
        keys = ["R1", "R2"] + (["R3"] if name == "parallel_resistance3" else [])
        return 1 / sum(
            (1 / positive(k, "resistance") for k in keys), Fraction()
        ), "resistance"
    if name == "source_voltage3":
        return sum(
            (value(k, "voltage") for k in ["U1", "U2", "U3"]), Fraction()
        ), "voltage"
    if name in {"mixed_resistance", "mixed_current"}:
        a, b, c = (positive(k, "resistance") for k in ["R1", "R2", "R3"])
        total = a + 1 / (1 / b + 1 / c)
        return (
            (total, "resistance")
            if name == "mixed_resistance"
            else (value("U", "voltage") / total, "current")
        )
    if name == "ohm_current":
        return value("U", "voltage") / positive("R", "resistance"), "current"
    if name == "ohm_voltage":
        return value("I", "current") * positive("R", "resistance"), "voltage"
    if name == "ohm_resistance":
        return positive("U", "voltage") / positive("I", "current"), "resistance"
    if name == "ohm_wire_current":
        return value("U", "voltage") * positive("S", "area") / (
            positive("rho", "resistivity") * positive("l", "length")
        ), "current"
    if name == "ohm_wire_length":
        return positive("U", "voltage") * positive("S", "area") / (
            positive("rho", "resistivity") * positive("I", "current")
        ), "length"
    if name == "ohm_wire_voltage":
        return value("I", "current") * positive("rho", "resistivity") * positive(
            "l", "length"
        ) / positive("S", "area"), "voltage"
    if name == "ohm_charge_resistance":
        return positive("U", "voltage") * positive("t", "time") / positive(
            "q", "charge"
        ), "resistance"
    if name == "ohm_electron_count":
        e = positive("e", "charge")
        if e != Fraction("1.6e-19"):
            raise ValueError("explicit_elementary_charge_magnitude")
        count = (
            value("U", "voltage")
            * value("t", "time")
            / (positive("R", "resistance") * e)
        )
        if count.denominator != 1:
            raise ValueError("whole_particle_count")
        return count, "dimensionless"
    if name == "mean_resistance4":
        return sum(
            (positive(k, "resistance") for k in ["R1", "R2", "R3", "R4"]), Fraction()
        ) / 4, "resistance"
    if name == "voltage_work":
        return value("A", "energy") / positive("q", "charge"), "voltage"
    if name == "electric_work":
        return value("q", "charge") * value("U", "voltage"), "energy"
    if name == "work_charge":
        return value("A", "energy") / positive("U", "voltage"), "charge"
    if name == "series_cells":
        count = positive("n", "dimensionless")
        if givens["n"]["unit"] != "1" or count.denominator != 1:
            raise ValueError("whole_cell_count_required")
        return count * positive("U0", "voltage"), "voltage"
    if name == "current_strength":
        return value("q", "charge") / positive("t", "time"), "current"
    if name == "current_charge":
        return value("I", "current") * value("t", "time"), "charge"
    if name == "current_time":
        return value("q", "charge") / positive("I", "current"), "time"
    if name in {"current_electron_count", "current_electron_mass"}:
        e = positive("e", "charge")
        if e != Fraction("1.6e-19"):
            raise ValueError("explicit_elementary_charge_magnitude")
        count = value("I", "current") * value("t", "time") / e
        if count.denominator != 1:
            raise ValueError("whole_particle_count")
        if name == "current_electron_mass":
            m0 = positive("m0", "mass")
            if m0 != Fraction("9.1e-31"):
                raise ValueError("explicit_electron_rest_mass")
            return count * m0, "mass"
        return count, "dimensionless"
    if name == "electric_work_current":
        return value("U", "voltage") * value("I", "current") * value(
            "t", "time"
        ), "energy"
    if name == "current_work_voltage":
        return value("A", "energy") / (
            positive("I", "current") * positive("t", "time")
        ), "voltage"
    if name == "wire_resistance":
        return positive("rho", "resistivity") * positive("l", "length") / positive(
            "S", "area"
        ), "resistance"
    if name == "wire_resistivity":
        return positive("R", "resistance") * positive("S", "area") / positive(
            "l", "length"
        ), "resistivity"
    if name == "wire_length":
        return positive("R", "resistance") * positive("S", "area") / positive(
            "rho", "resistivity"
        ), "length"
    if name == "wire_area":
        return positive("rho", "resistivity") * positive("l", "length") / positive(
            "R", "resistance"
        ), "area"
    if name == "field_charge":
        return value("F", "force") / positive("E", "electric_field"), "charge"
    if name == "field_electron_count":
        e = positive("e", "charge")
        if e != Fraction("1.6e-19"):
            raise ValueError("explicit_elementary_charge_magnitude")
        count = value("F", "force") / (e * positive("E", "electric_field"))
        if count.denominator != 1:
            raise ValueError("whole_particle_count")
        return count, "dimensionless"
    if name == "point_dielectric_ratio":
        k = positive("k", "coulomb_constant")
        if k != 9_000_000_000:
            raise ValueError("explicit_vacuum_coulomb_constant")
        ratio = (
            k
            * positive("q", "charge")
            / (positive("E", "electric_field") * positive("r", "length") ** 2)
        )
        if ratio < 1:
            raise ValueError("static_dielectric_model")
        return ratio, "dimensionless"
    if name == "field_balance_charge":
        if positive("g", "acceleration") != 10:
            raise ValueError("explicit_drop_g_is_10")
        return positive("m", "mass") * 10 / positive("E", "electric_field"), "charge"
    if name == "lightning_distance":
        if positive("v", "speed") != 340:
            raise ValueError("explicit_sound_speed_model_340")
        return 340 * value("t", "time"), "length"
    if name in {"charge_multiple", "electron_count"}:
        e = positive("e", "charge")
        if e != Fraction("1.6e-19"):
            raise ValueError("explicit_elementary_charge_magnitude")
        if name == "charge_multiple":
            count = value("n", "dimensionless")
            if givens["n"]["unit"] != "1" or count.denominator != 1:
                raise ValueError("whole_particle_count")
            return count * e, "charge"
        count = value("q", "charge") / e
        if count.denominator != 1:
            raise ValueError("whole_particle_count")
        return count, "dimensionless"
    if name == "particle_mass_sum":
        count = value("n", "dimensionless")
        mass = positive("m0", "mass")
        if (
            givens["n"]["unit"] != "1"
            or count.denominator != 1
            or mass not in {Fraction("9.1e-31"), Fraction("1.67e-27")}
        ):
            raise ValueError("explicit_particle_mass_and_whole_count")
        return count * mass, "mass"
    if name in {"coulomb_force", "field_point", "equal_coulomb_charge"}:
        k = positive("k", "coulomb_constant")
        if k != 9_000_000_000:
            raise ValueError("explicit_vacuum_coulomb_constant")
        radius = positive("r", "length")
        if name == "coulomb_force":
            return k * positive("q1", "charge") * positive(
                "q2", "charge"
            ) / radius**2, "force"
        if name == "field_point":
            return k * value("q", "charge") / radius**2, "electric_field"
        radicand = positive("F", "force") * radius**2 / k
        top, bottom = isqrt(radicand.numerator), isqrt(radicand.denominator)
        if top * top != radicand.numerator or bottom * bottom != radicand.denominator:
            raise ValueError("root_rounding_not_reviewed_for_this_rule")
        return Fraction(top, bottom), "charge"
    if name == "identical_charge2":
        return (projection("q1", "charge") + projection("q2", "charge")) / 2, "charge"
    if name == "equal_share_ratio":
        a, b = positive("q1", "charge"), positive("q2", "charge")
        return (a + b) ** 2 / (4 * a * b), "dimensionless"
    if name == "field_strength":
        return value("F", "force") / positive("q", "charge"), "electric_field"
    if name == "field_force":
        return value("E", "electric_field") * value("q", "charge"), "force"
    if name == "dielectric_field":
        eps = positive("eps", "dimensionless")
        if eps < 1:
            raise ValueError("static_dielectric_model")
        return value("E0", "electric_field") / eps, "electric_field"
    if name == "dielectric_ratio":
        e0, e = positive("E0", "electric_field"), positive("E", "electric_field")
        if e0 < e:
            raise ValueError("static_dielectric_model")
        return e0 / e, "dimensionless"
    if name in {
        "potential7",
        "gravity_work7",
        "mechanical_total7",
        "crane_efficiency7",
    }:
        m, g = positive("m", "mass"), positive("g", "acceleration")
        if g not in {Fraction("9.8"), Fraction(10)}:
            raise ValueError("explicit_grade7_energy_g")
        if name == "gravity_work7":
            return m * g * (value("h1", "length") - value("h2", "length")), "energy"
        e = m * g * value("h", "length")
        if name == "potential7":
            return e, "energy"
        if name == "mechanical_total7":
            return e + m * value("v", "speed") ** 2 / 2, "energy"
        eta = e / (positive("N", "power") * positive("t", "time"))
        if eta > 1:
            raise ValueError("efficiency_exceeds_one")
        return eta, "dimensionless"
    if name == "kinetic_change":
        return positive("m", "mass") * (
            value("v2", "speed") ** 2 - value("v1", "speed") ** 2
        ) / 2, "energy"
    if name == "spring_energy":
        return positive("k", "stiffness") * value("x", "length") ** 2 / 2, "energy"
    if name == "kinetic_balance":
        e = value("Ek1", "energy") + value("Ep1", "energy") - value("Ep2", "energy")
        if e < 0:
            raise ValueError("negative_kinetic_energy")
        return e, "energy"
    if name == "parallel_power":
        return value("F", "force") * value("v", "speed"), "power"
    if name == "power_force":
        return value("N", "power") / positive("v", "speed"), "force"
    if name == "linear_momentum":
        return positive("m", "mass") * projection("v", "speed"), "momentum"
    if name == "force_impulse":
        return projection("F", "force") * value("t", "time"), "momentum"
    if name == "momentum_change":
        return positive("m", "mass") * (
            projection("v", "speed") - projection("v0", "speed")
        ), "momentum"
    if name in {"momentum_sum2", "inelastic_velocity"}:
        m1, m2 = positive("m1", "mass"), positive("m2", "mass")
        p = m1 * projection("v1", "speed") + m2 * projection("v2", "speed")
        return (p, "momentum") if name == "momentum_sum2" else (p / (m1 + m2), "speed")
    if name == "recoil_velocity":
        return -positive("m", "mass") * projection("u", "speed") / positive(
            "M", "mass"
        ), "speed"
    if name == "directed_work":
        return projection("Fpr", "force") * value("s", "length"), "energy"
    if name == "lifting_lab_work":
        return positive("F", "force") * value("h", "length"), "energy"
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
