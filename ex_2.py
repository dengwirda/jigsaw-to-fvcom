
import os
import numpy as np
import netCDF4 as nc

import jigsawpy
from cullfvc import cullfvc
from savefvc import savefvc


def ex_2():

# DEMO-2: generate a simple mesh for the Saco bay coastline.

    rootpath = \
        os.path.abspath(
            os.path.dirname(__file__))

    src_path = \
        os.path.join(rootpath, "files")
    dst_path = \
        os.path.join(rootpath, "cache")


    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    hmat = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

    proj = jigsawpy.jigsaw_prj_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(dst_path, "geom.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "opts.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "mesh.msh")

    opts.hfun_file = \
        os.path.join(dst_path, "spac.msh")

    bnds_file = os.path.join(
        src_path, "saco_geom.msh")

    elev_file = os.path.join(
        src_path, "etop_cull.grd")

#------------------------------------ load coast + elevation

    jigsawpy.loadmsh(bnds_file, geom)

    elev = nc.Dataset(elev_file, "r")

#------------------------------------ define spacing pattern

    alon = np.array(elev.variables["x"][:],
                    dtype=hmat.REALS_t)
    alat = np.array(elev.variables["y"][:],
                    dtype=hmat.REALS_t)
    zlev = np.array(elev.variables["z"][:],
                    dtype=hmat.REALS_t)

#   setup a simple SQRT(g*H)-type mesh spacing pattern, with
#   the min/max values capped at HMIN/HMAX

    hmat.mshID = "ellipsoid-grid"
    hmat.radii = geom.radii

    hmat.xgrid = alon * np.pi / 180.
    hmat.ygrid = alat * np.pi / 180.

    hmin = +25.; hmax = +2000.; grav = +9.81

    hmat.value = +7.5 * \
        np.sqrt(np.maximum(-zlev * grav, 0.))

    hmat.value = \
        np.maximum(hmat.value, hmin)
    hmat.value = \
        np.minimum(hmat.value, hmax)

#   define a "smoothing" coefficient, to limit the allowable
#   gradient, smaller values give smoother patterns

    hmat.slope = np.full(
        hmat.value.shape, +0.0250,
        dtype=jigsawpy.jigsaw_msh_t.REALS_t)

#------------------------------------ do stereographic proj.

    geom.point["coord"] *= np.pi / 180.

#   transform from lon-lat coordinates to a "local" stereo-
#   graphic plane, both the geometry + spacing information
#   is transformed

    proj.prjID = 'stereographic'
    proj.radii = np.mean(geom.radii)
    proj.xbase = -70.333 * np.pi / 180.
    proj.ybase = +43.500 * np.pi / 180.

    jigsawpy.project(geom, proj, "fwd")
    jigsawpy.project(hmat, proj, "fwd")

    jigsawpy.savemsh(opts.geom_file, geom)
    jigsawpy.savemsh(opts.hfun_file, hmat)

#------------------------------------ set HFUN grad.-limiter

#   smooth the mesh spacing pattern, by limiting the maximum
#   gradient based on HMAT.SLOPE

    jigsawpy.cmd.marche(opts, hmat)

#------------------------------------ build mesh via JIGSAW!

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null h(x) limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.mesh_rad2 = +1.2               # relax thresholds
    opts.mesh_eps1 = +1.0               # a little

    opts.verbosity = +1

    jigsawpy.cmd.jigsaw(opts, mesh)

#------------------------------------ cull disconnected cell

    seed = np.array([[0, 0]])           # point "in" ocean

    cullfvc(mesh, seed)

#------------------------------------ write to output format

    print("Saving case_2a.dat file.")

    savefvc(os.path.join(
        rootpath, "case_2a.dat"), mesh)

    print("Saving case_2b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        rootpath, "case_2b.vtk"), mesh)

    jigsawpy.savevtk(os.path.join(
        rootpath, "case_2c.vtk"), hmat)

    return


if (__name__ == "__main__"): ex_2()
