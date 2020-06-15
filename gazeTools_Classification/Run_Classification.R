# Make sure gazetools and other necessary libraries are installed, if not run the following code"
# install.packages('devtools')
# library(devtools)
# devtools::install_github("ryanhope/gazetools")
# install.packages('data.table')
# install.packages('bit64')   # Install this package to be able to read Tobii files

# Parameters:
# Modify the following files inside config:
#   columns_output.txt: columns from input file to be retained in the output file
#   columns_process.txt: keep columns that are generally non-null, during processing
#   [Make sure columns_output.txt is a subset of the columns_process.txt]
# Set the values for the following variables:
#   data_folder: Contains all the raw tsv gaze-files.
#   ouput_location: location where to place the processed output files
#   gazetools_outputColumns: specifies folumns from gazetools obect to include in output
#                            look at gazetools_columns.txt under config for complete list
# Set appropriate parameters for the gazetools in line 45 of Gazetools_Classification_Script.R


# Import packages into workspace
library("gazetools")
library("Rcpp")
source("Gazetools_Classification_Script.R")

# Parameters for CTWC19 data
data_folder <- "/CogWorks/cwl-data/Active_Projects/Tetris/External_Tournaments/CTWC19/Tobii-LabPro/CTWC19_labpro_dataexport/"
ouput_location <- "/CogWorks/cwl-data/Active_Projects/Tetris/Workspaces/Banerjee/Gaze_Stuff/R_Files/Gaze_Outputs/CTWC19/"
input_files <- list.files(path=data_folder, pattern="*.tsv", full.names=TRUE, recursive=FALSE)
gazetools_outputColumns <- c("timestamp", "time", "x", "y", "class")
loop_through_files(input_files, ouput_location, gazetools_outputColumns)

