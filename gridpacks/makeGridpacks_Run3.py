import os


cwd = os.getcwd()
cards_path = 'cards/production/13p6TeV/NMSSM_XToYH_YToHH/'
mg_path = 'genprod_run3_slc7/bin/MadGraph5_aMCatNLO/'
os.chdir(mg_path)

# mass grid agreed by B2G dib / MC&I conveners:
# https://gitlab.cern.ch/cms-b2g/b-2-g-m-csample-requests/-/issues/6
X_mass = [240, 280, 300, 320, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2500, 2600, 2800, 3000, 3500, 4000]
Y_mass = [50, 60, 70, 80, 90, 95, 100, 125, 150, 170, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2300, 2400, 2600, 2800, 3000, 3300, 3500, 3800]


def is_mass_ok(m_x,m_y):
    return m_y >= 250. and m_y < (m_x-125.)


for mX in X_mass:

    for mY in Y_mass:
        if not is_mass_ok(mX,mY):
            continue
        print('(mX, mY)=({}, {})'.format(mX, mY))

        sample_name = 'NMSSM_XToYH_YToHH_MX_{}_MY_{}'.format(mX, mY)
        sample_cards_path = os.path.join(cards_path, sample_name)

        # run MadGraph
        cmd = 'time ./gridpack_generation.sh {} {} local'.format(sample_name, sample_cards_path)
        os.system(cmd)

        # move gridpack
        cmd = 'mv -v {} {}'.format(sample_name + '*_tarball.tar.xz', cwd)
        os.system(cmd)
