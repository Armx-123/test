from pytrends.request import TrendReq as UTrendReq
import pandas as pd

# Custom headers (you already defined them)
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://trends.google.com/trends/explore?date=now%201-d&gprop=youtube&q=memes&hl=en',
    'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-arch': '""',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '"Chromium";v="136.0.0.0", "Brave";v="136.0.0.0", "Not.A/Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Nexus 5"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"6.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
    'cookie': 'SOCS=CAISNQgQEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjQwNTE0LjA2X3AwGgJmaSADGgYIgOu0sgY; HSID=APfwK9naRL3piLzCE; SSID=A-sU45Y85OszCk78n; APISID=tqCnhEP6qfsN9mGa/AL49EbAiCFp1jr3OD; SAPISID=69k19-SG6Qb_uwWT/AIhIVCRtHLnVqt4va; __Secure-1PAPISID=69k19-SG6Qb_uwWT/AIhIVCRtHLnVqt4va; __Secure-3PAPISID=69k19-SG6Qb_uwWT/AIhIVCRtHLnVqt4va; SID=g.a000wQgzQ1uQJiSk1pyVUG5WdHiwnu8UyGAKjP2Fbvy6RIFnQuc7EZV197qm8WuLklUHd80XbQACgYKAaoSARcSFQHGX2Mi5DOmP1S0tYDPTKEDS0jKIRoVAUF8yKpCuv78Hxqk_TXyRsjOIWSM0076; __Secure-1PSID=g.a000wQgzQ1uQJiSk1pyVUG5WdHiwnu8UyGAKjP2Fbvy6RIFnQuc7FWH00E173I7QNx_W2ucIvQACgYKAU0SARcSFQHGX2Mi1CwTrm163P87jkQHzhlFAhoVAUF8yKqfl1yozeRGxSgYZ4FsvU_z0076; __Secure-3PSID=g.a000wQgzQ1uQJiSk1pyVUG5WdHiwnu8UyGAKjP2Fbvy6RIFnQuc751sqWdo0XTD8nq8qXOGo2AACgYKAZ4SARcSFQHGX2MiEXwWA8bIy7DrnHpyPXhDWhoVAUF8yKqeODclHF2MCZGa7KH4tHNb0076; AEC=AVcja2dOgwqkdZtwh0Av41OEZ4AOVHnt38NQfWl44U_3Y04-JdCEHTVJ7Eg; SEARCH_SAMESITE=CgQIgp4B; OTZ=8089673_34_34__34_; NID=524=oiBGl1IaG05Q7nQo5kozKevl661ofUl9xoczJbZkZ2YNw2DlCNQbn2Rlsr-hgJbQKD5YjsqvqmetFDXNxN7KLwzkD0rYC7qkgqtKFRgaK58Hu_bsOa8zsRsiAhd6CFZ7aIqcUkCnNu8zUHI9EkyiNcHriJgnGihP6udMUzy1762Dk7GbgaSh6_6Ex2rNXq1qKfMoW80yQa88LKeZKzBfFHgWfjqfkM_uh4HSH3TyoxyihzCLk91I2WA1FD1PYrIPc6yqvBTyXXfr9ZmBhoVICnhkQn1HCu3Az1nUSA2SlzYYhL1WKJdgH06soSnsCfkf8zFJa0sHYyzLYdoUBZn8ccAZ39JX_PemXQm_HVozyDFJyMzrCQVa18LZVp_yqQ04EX0koU1XcX5hh06PuDSWDtZv1IwoBiKuzg52PX0mXpbAC01FBv4z53P61jR_s1yvhcdgmh95EqDF46MR5yGhLTUb--yBYdiDbVu53XrxOwCKbf9c15FoLFWTqKxD2k6wPHqghuHbNKhd3fYhOjfRwiy0Ku1uC1x6x4TWslXN51EWekG9pTM3pghbp7pZPNXhY102DSBXGbMSFxHlLMUxtYg3P7Qy4EHvmYpFkkQAr8hT7FpI356HxNN5A7lhpOH43ZL_UdhpjLgmBNJZ8Sg-QKAxRXBF6DpKX1mZGHclf_oA013je5xSFq_8mGuncWHu0kOOrnk1bEh9qSxYmkfe4MkNcleoRQswO8yrMbp3bp-cKA3H9RLetkGWmdvEGsy_mAmEA3rJzEkQJGXt0GGtJXXoeOuMDhVYm5HJqYFwrQOSqxlbz37E68SvQ1PiZy1KzcQW9LhAH8NaxsntjeA9uUVydppuQ8bk9taSgv0SJb_4oVWbilf40uMD8yDZPzD1CgLLUVatz2EQJYc88mtXbIq4ONmpKz2w0zKzF4PTOvk5MSx9Lh8eC3EWaUZ1-4U-5d-nBhkYQSg7bw_ETV-s5yYAB1GdJtllbiIh3iqrxVNM_GdbTef2aBJzXTMDySvb7sSHS7fzirl27cAb68Y7GRAHbHkmWTjuzG7KnTbhES4vHmMdPt84xSLr94XExhDuixeoN_NlC7GocOfiGBF55j3_sKgP_RDTNQpVRzSIfhnGOkzW_-hqRI5DP1EGR4rAJTksUyxEv4BJpOD3fyWQ63Q7-6VEhOdhBJ0CFxwMmvgZW7g8_ATpK3qLUjtYv8MaG_KjS0E8ZQlCoyeHsrleyoP1fqq0tuqhGGhX8hAS9-bd7b83gcuqqiPPD1q09q4H1AdQTwCTwxpvKIh-xW6nmUUCU5sLPlfseuMIosA8DOL4fw589QZGhdFnQQy2HhuqAZod63SR0bWr_1LIaf6EAMY5VLceD7kbfR6f_k4Vov_alompcbBSYtyPknBDQMwk-QUzVm-Svy9DRm5DAnSZ-iNqLwx54SmZoYNr9G9zT_r6a3LP7-NN9YvXYYDMnRulWOJvb2aLPV_oey6-9M_Z064_iGeR4tZn7WBE-B_HwrgamhqOYmdJKuI83d275dA7OR5CDaMrEjrEQhjfMmCSynvNmb_SoRDluommIhNbJ5Pzi1E_Ry1BSBYeyctnkg7_lyQa6DP9iA9V76e1EfcLd9tK8CmlC7zNz5xuRTHFDw-uxSXEHRDCz9gqECkg1sMryd6xQLed1DOIn006vSM9OPHPgqwd8vLR5xJDgrVUs18S0MoR-oj5ppBKYdAG_EDJD16eGEETjATj1BaMt88r596nhhXTjcsFm9eSn1U4186rUeuUF6-QxkvG94fIJrkrs4bzQ8rpQhRTWGFInwJtVRznzlI_7gjmmR5yTmNrnUBJjTZCfLhFkXkvEHkF1bbUOc11viJweKoS8aYTkFLrMabYhQiuO-DEpG-9MZB1lzCUtqu4fFKUOcbU81sSzL_a50a_ix6vAcUam0th9qg_WTw3-A0R4ZpkeJy84AwPruTQQYSxpfZgSYemMI8-ssQeVyyi47hswkhTUFfO3GDgHPzLYsG2eCzpJ0MUrMmmUUWTjqgVjL9lTqvf40RbQRImTo9slDagXZ8E2ZY1mLUO9KSrDkNQu8UGdslmgo0dD_3x__TZRQEGDzfffR3SqevP7vr2GZHxpCkLndMDccP1PbhG6qOrXrwH5r_IGoI5MfXnpGoJfOxcnKa4wPrTfIIILmkD7BFrxqoXA5l7davtiKtQbl2zSqP7vVWt6ETPIBwxh5Rz_ukL-apbExQwBdhC_h1pkpPe85F39_vFi1YlT94aBIGzKOAGpSRqvD7SbOadAhqUhPE6nVaPx-qO7-mh-lOFDfOUNacY9nKWVmu6oQZd8fW5kAWT0Gp9mleSFDxOmZXAiZFcOUOdEsaA0XxgDxJpal0kUgOCrqaCZb5LDN34qtLf0HKFVsFQkjdgpwXtk3TOfqyHkZCwHDZ3gwkwa-NbXBfLRSeCUgcoP3hfZpEwZ2BjkShoZaD7eIquynPFUWqV6Pc7lB0fZhAGfCxvuukAFR1tcQlt0mar59ON9NZAHH_Uze9rJw0rhX0Nil8gLWk1545ZXZxY4fI0KT7YjdiJF7L8txA5E5Pv_6AxY597yESvkuAfZmNlz8cixRHBrPDsf6brZciwRIWgaoU1RlGdDWk7_6oYP1uL71wdzgD5X0sQOfC8oAw44RwcN06EssMFMxzy9Unv_A_6CWAOegajiusB2KuTJS1PbvDBxp_hs-oe0-DGt-iNQC5n8NhdOfwgWxrfkkwm4-SsV_5_Nm1jHulZnxc4gWk4sIekMsYC7e-EXLel5TykdYgfO6bPQ1EwdQ9RgJTpmUmJrZec0NCAgM1MxSRCnZ1TIKNbQ9qwkHmJNtGU-LsV; __Secure-1PSIDTS=sidts-CjEBjplskG_lqldWXWg-iIgLGOcQH9RHWfcVG1EVUgYagN9W9ojYFBfwtTNq_9Mk6XXZEAA; __Secure-3PSIDTS=sidts-CjEBjplskG_lqldWXWg-iIgLGOcQH9RHWfcVG1EVUgYagN9W9ojYFBfwtTNq_9Mk6XXZEAA; SIDCC=AKEyXzWtGj04FLMErHSF-SGtcnjrry2hAw1l3GPxPZboi4sA7mfwuztTDRKjfqH7yydgzRfkQA; __Secure-1PSIDCC=AKEyXzXsbBwxn5imUF9N_lWAa_KJLrjp_bD5QHfC-MyvyhoRTx9WtbjrKJIksTHDRG_Lw21uvw; __Secure-3PSIDCC=AKEyXzX6zOfN7cq-8DKQhg84sMSo2lHaz18y3kPf20eJ5bdimAGkt3YO1NXCM0eLkJ0zUjlF1Sc',
}

# Custom TrendReq that injects headers into _get_data
class TrendReq(UTrendReq):
    def _get_data(self, url, method='get', trim_chars=0, **kwargs):
        return super()._get_data(url, method=method, trim_chars=trim_chars, headers=headers, **kwargs)

# Use your custom TrendReq
pytrends = TrendReq(hl='en-US', tz=360,retries=3)

# Build the request
pytrends.build_payload(kw_list=['memes'], cat=182, timeframe='now 1-d', gprop='youtube')

# Get data
df = pytrends.interest_over_time()

# Fill and print
df = df.fillna(False).infer_objects(copy=False)
print(df.tail())
