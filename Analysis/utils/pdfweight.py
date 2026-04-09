import awkward as ak
import numpy as np


def get_pdf_unc(pdf_weights):
    # Eq. 21 in https://arxiv.org/pdf/1510.03865v2.pdf
    pdf_replicas = pdf_weights[:, 1:101]  # shape (nEvents, 100)
    # Mean of MC replicas
    pdf_mean = ak.mean(pdf_replicas, axis=1)
    # Standard deviation (MC replicas definition)
    pdf_std = ak.std(pdf_replicas, axis=1, ddof=1)

    return (pdf_std / pdf_mean)


def add_pdf_weights(events, weights):
    """
    PDF variation weights for the standard Hessian set
    """
    nom = ak.ones_like(weights.weight())

    pdf_weights = getattr(events, "LHEPdfWeight", None)

    if pdf_weights is not None:
        try:
            # NNPDF31_nnlo_as_0118_nf_4_mc_hessian
            # https://lhapdfsets.web.cern.ch/current/NNPDF31_nnlo_as_0118_nf_4_mc_hessian/NNPDF31_nnlo_as_0118_nf_4_mc_hessian.info
            # LHA IDs: 325500 - 325600
            if len(pdf_weights[0])==101:
                # PDF weights
                pdf_unc = get_pdf_unc(pdf_weights)
                weights.add('PDF_weight', nom, nom + pdf_unc, nom - pdf_unc)

                # alpha_S weights (NOT AVAILABLE)
                weights.add('aS_weight', nom)

                # PDF + alpha_S weights (NOT AVAILABLE)
                weights.add('PDFaS_weight', nom)
            # NNPDF31_nnlo_hessian_pdfas
            # https://lhapdfsets.web.cern.ch/current/NNPDF31_nnlo_hessian_pdfas/NNPDF31_nnlo_hessian_pdfas.info
            # LHA IDs: 306000 - 306102
            else:
                # PDF weights
                pdf_unc = get_pdf_unc(pdf_weights)
                weights.add('PDF_weight', nom, nom + pdf_unc, nom - pdf_unc)

                # alpha_S weights
                # Eq. 27 in https://arxiv.org/pdf/1510.03865v2.pdf
                as_unc = 0.5*(pdf_weights[:,102] - pdf_weights[:,101])
                weights.add('aS_weight', nom, nom + as_unc, nom - as_unc)

                # PDF + alpha_S weights
                # Eq. 28 in https://arxiv.org/pdf/1510.03865v2.pdf
                pdfas_unc = np.sqrt(np.square(pdf_unc) + np.square(as_unc))
                weights.add('PDFaS_weight', nom, nom + pdfas_unc, nom - pdfas_unc)

        except Exception as e:
            print("PDF variation structure unexpected:", e)
            print("PDF variation vector has length ", len(pdf_weights[0]))
    else:
        weights.add('PDF_weight', nom)
        weights.add('aS_weight', nom)
        weights.add('PDFaS_weight', nom)
