# Get list of column names in a data table
colnames(data.table)

# Get the number of non-empty rows for each column in a data.table
colSums(!is.na(data.table))
