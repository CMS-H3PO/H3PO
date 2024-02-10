import os


mass_points = [(2500, 2300), (3500, 3000), (3500, 3300), (4000, 3000), (4000, 3500), (4000, 3800)]

mg_path = 'genprod_mg265UL_slc7/bin/MadGraph5_aMCatNLO/'
os.chdir(mg_path)
    
for (mX, mY) in mass_points:
    print('(mX, mY)=({}, {})'.format(mX, mY))

    cards_path = 'cards/production/2017/13TeV/'

    sample_name = 'NMSSM_XYH_YToHH_MX_{}_MY_{}'.format(mX, mY)
    sample_cards_path = os.path.join(cards_path, sample_name)

    # run MadGraph
    cmd = 'time ./gridpack_generation.sh {} {} local'.format(sample_name, sample_cards_path)
    os.system(cmd)
