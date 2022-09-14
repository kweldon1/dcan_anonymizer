#!/usr/bin/env python
"""

A simple program to anonymize all dicom files in the supplied folder.

Usage: 

Created: Ron Yang for HBCD Pilot data .

"""
import argparse
import datetime
import itertools
import json
import logging as log
import os
import sys
import pydicom



CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
log.basicConfig(
        filename=os.path.join(CURRENT_DIR,  os.path.basename(__file__) + ".log"),
        format="%(asctime)s  %(levelname)10s  %(message)s",
        level=log.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Anonymize the HBCD Pilot data with a folder.")

    parser.add_argument('--input','-i', required=True,
            help="Input directory for original files.")
    parser.add_argument('--target-dir', '-t',required=True,
            help="Output dir for anonymized files.")

    parser.add_argument('--patient-name', '-p', default=None, required=True,
            help="Anonmized Patient name")

    parser.add_argument('--patient-id', '-d',default=None,
            help='Anonymized Patient ID.')
    parser.add_argument('--patient-age', '-a',default=None,required=True,
            help='Anonymized Patient Age in Weeks.')

    return parser.parse_args()

def ensure_directory(root, *args):
    """
    Return valid directory path and, if it does not exist, create it
    """
    export_dir = os.path.join(root, *args)
    if not os.path.isdir(export_dir):  # makedirs -> OSError if leaf dir exists
        os.makedirs(export_dir)  # could still raise OSError for permissions
    return export_dir


if __name__ == "__main__":
    args = parse_arguments()

    log.info('Started run with invocation: %s', sys.argv)

    # Determine what the base directory is and create it if needed
    if args.target_dir:
        target_dir = ensure_directory(args.target_dir)
    if not args.input:
        log.critical('Input Dir is not existed: %s', args.input)



    for x in os.listdir(args.input):
        #print(os.path.join(CURRENT_DIR,args.input, x), " target ", os.path.join(CURRENT_DIR, args.target_dir,  x))
        target_dir = ensure_directory(os.path.join(CURRENT_DIR, args.target_dir,  x))
        command = "dicom-anonymizer --keepPrivateTags " +  os.path.join(CURRENT_DIR,args.input, x) + " " +  target_dir 

        print(command)
        os.system(command)
        if args.patient_name:
           command2 = 'dcmodify -i "(0010,0010)='+ args.patient_name+ '" -nb ' + target_dir + '/*'
           os.system(command2)
           log.info("Anonymize Patient Name for this folder: %s", x)
        if args.patient_id:
           command3 = 'dcmodify -i "(0010,0020)='+ args.patient_id+ '" -nb ' + target_dir + '/*'
           os.system(command3)
           log.info("Anonymize Patient ID for this folder: %s", x)
 
        if args.patient_age:
           command4 = 'dcmodify -i "(0010,1010)='+ args.patient_age+ '" -nb ' + target_dir + '/*'
           os.system(command4)
           log.info("Anonymize Patient Age for this folder: %s", x)
 
        
       
        log.info("Completed anonymize this folder: %s", x)


    log.info('Ended run with invocation: %s', sys.argv)

