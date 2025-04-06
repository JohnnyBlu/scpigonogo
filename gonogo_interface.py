# gonogo_interface.py
# Version: 0.2.0

from rpy2.robjects import r, globalenv, FloatVector, NULL
from common import TrialResult

class GonogoInterface:
    def __init__(self, gonogo_path="gonogo.R", mlo=0.0, mhi=0.0, sg=0.0, test_type=2, reso=0.01):
        print("Loading gonogo.R...")
        r.source(gonogo_path)
        self.mlo = mlo
        self.mhi = mhi
        self.sg = sg
        self.test_type = test_type
        self.reso = reso
        self.z = None
        print("gonogo.R loaded.")

    def start_test(self):
        print(f"Starting gonogo test: mlo={self.mlo}, mhi={self.mhi}, sg={self.sg}, test={self.test_type}")
        self.z = r["gonogo"](
            mlo=self.mlo, mhi=self.mhi, sg=self.sg,
            test=self.test_type, reso=self.reso, Y=NULL
        )
        globalenv["z"] = self.z

    def record_result(self, result: TrialResult):
        if self.z is None:
            raise RuntimeError("gonogo session not initialized.")

        Y = self.z.rx2("d0").rx2("Y")
        X = self.z.rx2("d0").rx2("X")
        new_Y = FloatVector(list(Y) + [1.0 if result.go else 0.0])
        new_X = FloatVector(list(X) + [result.stimulus_level])

        self.z = r["gonogo"](
            mlo=0, mhi=0, sg=0,
            test=self.test_type, reso=self.reso,
            newz=False, Y=new_Y, X=new_X
        )
        globalenv["z"] = self.z

    def get_next_stimulus(self):
        if self.z is None:
            raise RuntimeError("gonogo session not initialized.")
        rx = self.z.rx2("d0").rx2("RX")
        return float(rx[-1]) if len(rx) else None

    def get_mu_sigma(self):
        if self.z is None:
            return None, None
        if "musig" in self.z.names:
            musig = self.z.rx2("musig")
            return float(musig[0]), float(musig[1])
        return None, None

    def has_converged(self, threshold=0.01, prev_estimates=None):
        mu, sigma = self.get_mu_sigma()
        if mu is None or sigma is None or prev_estimates is None:
            return False, (mu, sigma)
        prev_mu, prev_sigma = prev_estimates
        converged = abs(mu - prev_mu) < threshold and abs(sigma - prev_sigma) < threshold
        return converged, (mu, sigma)
