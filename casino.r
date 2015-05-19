gen1 <- c(1,2,3,4,5)
gen2 <- c(1,2,3,4,5,6,6,6,6,6,6)

genSeq <- function(length, prob1) {
  result <- matrix(nrow = 2, ncol = length)
  for (i in 1:length) {
    if (runif(1,0,1) <= prob1) {
      result[1,i] = sample(gen1,1)
      result[2,i] = 1
    } else {
      result[1,i] = sample(gen2,1)
      result[2,i] = 2
    }
  }
  return(result)
}

bhattacharyyaDistance <- function(first, second) {
  dist <- 0
  l1 <- length(first)
  l2 <- length(second)
  domain <- unique(c(first,second))
  for (i in domain) {
    dist <- dist + sqrt(sum(first==i)*sum(second==i)/(l1*l2))
  }
  return(-log(dist))
}

bhD <- bhattacharyyaDistance

length <- 1000
prob <- 0.33
seq <- genSeq(length,prob)
bestD <- -1

for (i in 1:10000) {
  bs <- sample(1:2,length,replace=TRUE)
  first <- sum(bs==1)
  second <- sum(bs==2)
  firstProbable <- seq[1,bs==1]
  secondProbable <- seq[1,bs==2]
  dist <- bhD(firstProbable, secondProbable)
  
  if (bestD < dist) {
    best <- bs
    bestD <- dist
  }
}

