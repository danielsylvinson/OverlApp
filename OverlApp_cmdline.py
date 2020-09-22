from orbkit import read
from orbkit import options, main, grid
from orbkit import analytical_integrals
import orbkit
import numpy
import sys
import re
import glob
import os
from cubature import cubature

filein = sys.argv[2:]
v = sys.argv[1]
try:
    printed = ["Note: If the mean error of any of the computed integrals is large, consider increasing max. evaluations value\n"]
    printed.append("=============================================================\n")
    printed.append("Filename                      Overlap Integral           Mean Absolute Error \n")
    numproc = 1             #: Specifies number of subprocesses.
    slice_length = 1e4
    infile = filein
    print(infile)

    filenames_RPA_singlet = sorted(infile)
    for filename in filenames_RPA_singlet:
        fullpath, just_filename = os.path.split(filename)
        orbkit.options.quiet = True
        orbkit.options.no_log = True
        pattern = "[GTO]"
        lines = []
        num=0
        with open(filename, "r") as f:
            lines1 = f.readlines()
            for line in lines1:
                if num == 0:
                    lines.append(line.lstrip())
                elif num == 1:
                    lines.append(line)
                if pattern in line:
                    num = 1
        f.close()
        filename2 = "RPA_S" + ".molden"
        with open(filename2, "w") as f:
            f.writelines(lines)
        f.close()

        qc = read.main_read(filename2,all_mo=True)
        orbkit.init()
        orbkit.options.quiet = True
        orbkit.options.no_log = True
        orbkit.options.calc_mo = [1]
        orbkit.options.filename = filename2
        orbkit.options.adjust_grid = [5, 0.5]
        data = orbkit.run_orbkit()
        xl = numpy.amin(orbkit.grid.x)
        yl = numpy.amin(orbkit.grid.y)
        zl = numpy.amin(orbkit.grid.z)
        xh = numpy.amax(orbkit.grid.x)
        yh = numpy.amax(orbkit.grid.y)
        zh = numpy.amax(orbkit.grid.z)
        eig = [ sub['energy'] for sub in qc.mo_spec]
        fdim=len(qc.mo_spec)/2
        fdim = int(fdim)
        i = numpy.argsort(eig)
        j = i[::-1]
        orbkit.init()
        orbkit.options.quiet = True
        orbkit.options.no_log = True
        orbkit.grid.is_initialized = True


        def func(x_array,*args):
          x_array = x_array.reshape((-1,3))
          orbkit.grid.x = numpy.array(x_array[:,0],copy=True)
          orbkit.grid.y = numpy.array(x_array[:,1],copy=True)
          orbkit.grid.z = numpy.array(x_array[:,2],copy=True)


          out = orbkit.rho_compute(qc,
                                   calc_mo=True,
                                   slice_length=slice_length,
                                   drv=None,
                                   laplacian=False,
                                   numproc=numproc)
          out1 = out[i]
          out2 = out[j]
          out1 = numpy.abs(out1)
          out2 = numpy.abs(out2)

          out=out1[:fdim]*out2[:fdim]
          return out.transpose()
        ndim = 3
        xmin = numpy.array([xl,yl,zl],dtype=float)
        xmax = numpy.array([xh,yh,zh],dtype=float)
        abserr = 1e-15
        relerr = 1e-5
        integral_mo,error_mo = cubature(func, ndim, fdim, xmin, xmax, args=[],adaptive='h', abserr=abserr, relerr=relerr, norm=0, maxEval=v, vectorized=True)
        coeff = numpy.sort(eig)[:fdim]
        sum = numpy.sum(numpy.abs(coeff))
        norm_integral_mo = (numpy.abs(coeff)*integral_mo)/sum
        delta = numpy.sum(norm_integral_mo)
        mae = numpy.mean(numpy.abs(error_mo))
        print(str(just_filename) + "\n" + "Overlap: " + str("%.5f" % delta) + " MAE: " + str("%.5f" % mae) + "\n")
        printed.append(str(just_filename) + "                    " + str("%.5f" % delta) + "                           " + str("%.5f" % mae) + "\n")

    printed.append("Job completed! \n")
    printed.append("====================================================================\n")

    print(printed)
    with open(os.path.join(fullpath,'Overlap.txt'),'w') as fw:
        fw.writelines(("%s\n" % k for k in printed))
    fw.close()

except:
    printed = ["\n Oops! Something went wrong! \n"]
    print("\n Oops! Something went wrong! \n")
    printed.append("====================================================================\n")
