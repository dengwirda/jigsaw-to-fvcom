
import os
import numpy as np

import jigsawpy
from cullfvc import cullfvc
from savefvc import savefvc


def ex_1():

# DEMO-1: generate a non-uniform mesh for a box-type domain.

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

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(dst_path, "geom.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "opts.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "mesh.msh")

    opts.hfun_file = \
        os.path.join(dst_path, "spac.msh")

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +2
    geom.vert2 = np.array([ # list of xy "node" coordinate
        ((0, 0), 0),        # outer square
        ((9, 0), 0),
        ((9, 9), 0),
        ((0, 9), 0),
        ((4, 4), 0),        # inner square
        ((5, 4), 0),
        ((5, 5), 0),
        ((4, 5), 0)],
        dtype=geom.VERT2_t)

    geom.edge2 = np.array([ # list of "edges" between vert
        ((0, 1), 0),        # outer square
        ((1, 2), 0),
        ((2, 3), 0),
        ((3, 0), 0),
        ((4, 5), 0),        # inner square
        ((5, 6), 0),
        ((6, 7), 0),
        ((7, 4), 0)],
        dtype=geom.EDGE2_t)

    jigsawpy.savemsh(opts.geom_file, geom)

#------------------------------------ define spacing pattern

    xgeo = geom.vert2["coord"][:, 0]
    ygeo = geom.vert2["coord"][:, 1]

    xpos = np.linspace(                 # via regular grid
        xgeo.min(), xgeo.max(), 32)

    ypos = np.linspace(
        ygeo.min(), ygeo.max(), 16)

    xmat, ymat = np.meshgrid(xpos, ypos)

    hfun = -0.2 * np.exp(-(             # mesh size target
        0.1 * (xmat - 4.5) ** 2 +
        0.1 * (ymat - 4.5) ** 2)) + 0.3

    hmat.mshID = "euclidean-grid"       # into jigsaw data
    hmat.ndims = +2
    hmat.xgrid = np.array(
        xpos, dtype=hmat.REALS_t)
    hmat.ygrid = np.array(
        ypos, dtype=hmat.REALS_t)
    hmat.value = np.array(
        hfun, dtype=hmat.REALS_t)

    jigsawpy.savemsh(opts.hfun_file, hmat)

#------------------------------------ build mesh via JIGSAW!

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.cmd.jigsaw(opts, mesh)

#------------------------------------ cull disconnected cell

    seed = np.array([[2, 2]])           # point "in" ocean

    cullfvc(mesh, seed)

#------------------------------------ write to output format

    print("Saving case_1a.dat file.")

    savefvc(os.path.join(               # for FVCOM
        rootpath, "case_1.dat"), mesh)

    print("Saving case_1b.vtk file.")

    jigsawpy.savevtk(os.path.join(      # for eg. paraview
        rootpath, "case_1.vtk"), mesh)

    return


if (__name__ == "__main__"): ex_1()
