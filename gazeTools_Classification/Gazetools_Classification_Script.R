# Create a counter variable to keep track of the number of files processed
counter <- 1



# Function to loop through multiple gaze files and store prossed data given an input and output directory
loop_through_files <- function(input_files, ouput_location, gazetools_outputColumns) {
  # Reset counter everythime this function is called
  counter <<- 1
  
  # Set working directory to the location of this scrip
  library("rstudioapi") 
  setwd(dirname(getActiveDocumentContext()$path))
  
  # Get the list of columns to keep during processing
  keep_columns <- scan("configs/columns_process.txt", what="character", sep="\n")
  print("Read columns_process.txt")
  
  # Get the list of columns to keep in output file
  output_columns <- scan("configs/columns_output.txt", what="character", sep="\n")
  print("Read columns_output.txt")
  
  # Call the function over all files if the location
  emptyVariable <- lapply(input_files, get_clasified_gazeData, output_location=ouput_location,
                          keep_columns=keep_columns, output_columns=output_columns, 
                          file.count=length(input_files), gazetools_outputColumns=gazetools_outputColumns)
}



# Function to parse raw gaze-files and generate clssified gaze-files
get_clasified_gazeData <- function(input_file, output_location, keep_columns, 
                                   output_columns, file.count, gazetools_outputColumns) {
  # Read file into a data.table
  try(data <- fread(file=input_file, sep="\t", sep2=",", header = T, showProgress = F,
                na.strings=c("NA","", "None"), fill=TRUE), silent = FALSE) #TODO: determine if "Fill" screws things up
  data.dt <- data.table(data)

  # Only keep columns listed in the columns_process file, this is important because:
  # If mostly empty columns are kept the data.table goes empty while removing blinks
  keep_columns <- intersect(colnames(data.dt), keep_columns) # get intersection of two lists, in case keep columns has extra column names
  data.dt <- data.dt[, ..keep_columns]      # Removes columns, except those listed in colums_process.txt
  data.dt <- data.dt[complete.cases(data.dt), ] # Removes all blinks

  # to get the descriptions for each parameter run '?pva'
  # These parameters have been set according to the CTWC19 eye-tracking data
  gazetoolsObject <- gazetools(x=data.dt$`Gaze point X`,
                y= data.dt$`Gaze point Y`,
                samplerate=300,             # CTWC19 recording frequency
                rx=1920, ry=1080,           # Tobii monitor specs
                sw=527, sh=296,             # Tobii monitor specs
                ez=data.dt$`Eye position left Z (DACSmm)`, ex = data.dt$`Eye position left X (DACSmm)`, ey= data.dt$`Eye position left Y (DACSmm)`, 
                blinks=(data.dt$`Gaze point X`==0 & data.dt$`Gaze point Y`==0),
                timestamp=data.dt$`Recording timestamp`)

  yay_we_did_it <- gazetoolsObject$classify()
  gazetoolsData <- gazetoolsObject$`.->data`
  
  # Test if something went wrong while processing the file
  if (nrow(data.dt) != length(yay_we_did_it)) {
    print("gazetools output and original length of data donot match")
  }

  # Create Data-Table for output file
  #   Inner Join raw-data with gazetools-data on timestamp
  #     Set join columns
  setkey(gazetoolsData, timestamp)
  setkey(data.dt, `Recording timestamp`)
  #     Perform Join
  outputData <- gazetoolsData[data.dt, nomatch=0]
  #   Make sure output_columns is subset of outputData
  output_columns <- intersect(output_columns, colnames(outputData))
  #   Add gazetools data to output
  output_columns <- c(gazetools_outputColumns, output_columns)
  outputData <- outputData[, ..output_columns]
  
  input_file_name <- tail(strsplit(input_file, "/")[[1]], 1)    # get file name from path
  input_file_name <- strsplit(input_file_name, "[.]")[[1]][1]   # remove extension from file name
  output_file_name <- paste(input_file_name, "gazeTools_output.tsv", sep = " ")
  output_file_path <- paste(output_location, output_file_name, sep = "/")
  
  try(fwrite(outputData, output_file_path, sep = "\t", sep2 = c("","|","")))
  print(paste("done processing ", counter, "/", file.count, " files, finished file: ", input_file_name, sep = ""))
  counter <<- counter+1
}




# Test-Case for get_clasified_gazeData: Ignore
# data_folder <- "Sample_testData"
# filename <- "CTWC19 Recording5 19CTWC001.tsv"
# input_file <- paste(data_folder,filename,sep="/")
# output_location <- "Sample_testData"
# keep_columns <- scan("columns_process.txt", what="character", sep="\n")
# output_columns <- scan("columns_output.txt", what="character", sep="\n")
# counter <- 1
# get_clasified_gazeData(input_file, output_location, keep_columns, output_columns, 1)