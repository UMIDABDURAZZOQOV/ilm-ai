"""Explicit hypothetical demand model, never a claim of measured capacity."""
import json
import math


def scenarios():
    result = []
    for registered in (1000, 10000, 100000, 1000000):
        mau, dau = registered*.5, registered*.1
        concurrent = math.ceil(dau*.15*600/3600)
        rps = concurrent*.1
        result.append(dict(registered=registered, assumed_mau=round(mau), assumed_dau=round(dau),
            assumed_peak_concurrent=concurrent, core_rps=rps,
            login_rps=round(dau*.15/3600,4), catalogue_rps=round(rps*.2,3),
            mcq_frq_rps=round(rps*.4,3), progress_write_rps=round(rps*.3,3),
            profile_rps=round(rps*.1,3), ai_rps=round(concurrent/180,3),
            assumed_db_connections_with_3x_headroom=max(1,math.ceil(rps*.8*.05*3)),
            assumed_cpu_cores_at_60_percent=round(rps*.01/.6,3)))
    return dict(status='PLANNED', assumptions=dict(mau_share=.5,dau_share=.1,peak_hour_dau_share=.15,
        session_seconds=600,core_requests_per_active_user_per_second=.1,
        ai_explanation_interval_seconds=180,db_request_share=.8,db_hold_seconds=.05,
        average_cpu_seconds_per_core_request=.01),
        limitation='DAU ratios, DB hold and CPU service time are assumptions, not measured production data. '
                   'Component ASGI results must not be used to claim main:app capacity.', scenarios=result)


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(scenarios(), indent=2)+'\n'
    if args.output:
        args.output.write_text(result, encoding='utf8')
    else:
        print(result)
