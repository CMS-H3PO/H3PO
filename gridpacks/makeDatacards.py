from __future__ import print_function

import os, glob


# Script for replacing X->YH MG5 template cards with actual mass points (based on https://github.com/cms-sw/genproductions/blob/mg265UL/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/NMSSM_XToYH/getAllMassPoints_YH.py)

process = 'NMSSM_XYH_YToHH_MX_*_MY_*'
cards_dir = 'genprod_mg265UL_slc7/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/'

template_process = 'NMSSM_XYH_YToHH_MX_1200_MY_500'
template_dir = os.path.join(cards_dir, template_process)

if not os.path.isdir(template_dir):
    os.makedirs(template_dir)

    github_url = 'https://github.com/cms-sw/genproductions/raw/f3ddd04e5d91aca221b0df6d8cae728b97701935/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/NMSSM_XYH_YToHH_MX_1200_MY_500/'

    for card in [
        'NMSSM_XYH_YToHH_MX_1200_MY_500_customizecards.dat',
        'NMSSM_XYH_YToHH_MX_1200_MY_500_extramodels.dat',
        'NMSSM_XYH_YToHH_MX_1200_MY_500_proc_card.dat',
        'NMSSM_XYH_YToHH_MX_1200_MY_500_run_card.dat'
    ]:
        cmd = 'wget {} -P {}'.format((github_url + card), template_dir)
        os.system(cmd)
            
cards = glob.glob(os.path.join(template_dir,process))

for card in cards:
    print(card)

mass_points = [(2500, 2300), (3500, 3000), (3500, 3300), (4000, 3000), (4000, 3500), (4000, 3800)]

def is_mass_ok(m_x,m_y):
    return m_y < (m_x-125.)

Ngridpacks=0
for (mX, mY) in mass_points:
        if not is_mass_ok(mX,mY):
            continue
        print('(mX, mY)=({}, {})'.format(mX, mY))
        Ngridpacks+=1

        outdir = os.path.join(cards_dir, process.replace('MX_*_MY_*','MX_{}_MY_{}'.format(mX,mY)))

        if not os.path.isdir(outdir):
            os.makedirs(outdir)

        for card in cards:
            src_file = card
            tgt_file = os.path.join(outdir, os.path.basename(src_file).replace('MX_1200_MY_500','MX_{}_MY_{}'.format(mX,mY)))

            print('{} -> {}'.format(src_file,tgt_file))

            src_txt = open(src_file, 'r').read()

            if 'proc_card' in card:
                tgt_txt = src_txt.replace('MX_1200', 'MX_{}'.format(mX)).replace('MY_500', 'MY_{}'.format(mY))
            elif 'customizecards' in card:
                tgt_txt = src_txt.replace('45 1200', '45 {}'.format(mX)).replace('35 500', '35 {}'.format(mY))
            else:
                tgt_txt = src_txt
            
            with open(tgt_file, 'w') as f:
                f.write(tgt_txt)

print(Ngridpacks) 
