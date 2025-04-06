#!/usr/bin/env Rscript
suppressMessages(library(jsonlite))
suppressMessages(library(gonogo))

args <- commandArgs(trailingOnly = TRUE)
trial_json <- args[1]
state_file <- args[2]

trial <- fromJSON(trial_json)

# Load or initialize gonogo object
if (file.exists(state_file)) {
  gng <- readRDS(state_file)
} else {
  mu_est <- trial$mu_est
  sigma_est <- trial$sigma_est
  gng <- testplan(
    method = "neyer",
    distribution = "normal",
    xstart = mu_est,
    xinc = sigma_est / 2,
    ndose = 100,
    nmax = 50
  )
}

# Add trial data if available
if (!is.null(trial$stimulus) && !is.null(trial$response)) {
  gng <- gonogo(gng, x = trial$stimulus, y = trial$response)
}

saveRDS(gng, state_file)

result <- list(
  stimulus = if (!is.null(gng$nextdose)) gng$nextdose else NA,
  done = is.null(gng$nextdose),
  trials_so_far = length(gng$dose),
  max_trials = gng$nmax
)

# Return model fit info if available
if (!is.null(gng$fit)) {
  coefs <- coef(gng$fit)
  if ("(Intercept)" %in% names(coefs) && "dose" %in% names(coefs)) {
    beta0 <- coefs["(Intercept)"]
    beta1 <- coefs["dose"]
    result$mu <- -beta0 / beta1
    result$sigma <- 1 / beta1

    conf <- tryCatch({
      suppressMessages(confint(gng$fit))
    }, error = function(e) NULL)

    if (!is.null(conf)) {
      result$confint_mu <- unname(-conf["(Intercept)", ] / conf["dose", ])
    }
  }
}

cat(toJSON(result, auto_unbox = TRUE, digits = 6))
