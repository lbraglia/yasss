export <- function(df, fname) {
  write.csv(df, file=sprintf("%s.csv", fname), row.names=FALSE)
}
