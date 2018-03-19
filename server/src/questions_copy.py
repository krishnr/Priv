def get_question(dim):
    dim_to_question = {
    "Log Files": "Builds log files about my usage of the site?",
    "Activity": "Tracks web pages I visited before or after I come to this site?",
    "Opt Out": "Prohibits opt out of specific tracking approaches?",
    "Request": "Can request information collected about me?",
    "Cookies": "Uses cookies to create a web profile about me?",
    "Deletion": "Keeps my data after I delete my account?",
    "Disclosure": "Discloses my information for legal purposes without a warrant?",
    "Do Not Track": "Ignores ‘Do Not Track’ signals?",
    "Identification": "Collects my IP address or device ID?",
    "Policy Change": "Can update privacy policy without notifying me?",
    "Retention": "Retains data indefinitely?",
    "Security": "Stores data securely?",
    "Social Media": "Accesses my social media profiles?",
    "Targeted Advertising": "Performs targeted advertising?", 
    "Analysis": "Performs analysis on data collected about me?",
    "Collection": "Collects data about me?",
    "3P Sharing": "Shares my data with third parties?",
    "Location": "Tracks my location?",
    "Contact Info": "Collects my contact information?",
    "Personalization": "Uses my data to personalize content?",
    "Payment": "Collects my payment information?"
    }

    return dim_to_question[dim]

def get_question_desc(dim):
    dim_to_question_desc = {
    "Log Files": "This question identifies whether the service builds a list of your activity on their site.",
    "Activity": "This question identifies whether the service tracks the web pages you visit immediately before and after you come to site.",
    "Opt Out": "This question identifies whether the service allows you to opt out of specific tracking approaches, such as cookies.",
    "Request": "This question identifies whether the service allows you to request information on what data they have collected about you.",
    "Cookies": "This question identifies whether the service uses advertisement cookies or web beacons to collect more information about you.",
    "Deletion": "This question identifies whether the service keeps aspects of your data after you delete your account.",
    "Disclosure": "This question identifies whether the service requires a warrant for content when receiving government request for data. Read more about requiring a warrant for personal information <a href='https://www.eff.org/deeplinks/2017/06/eff-sec-get-warrant'>here</a>.",
    "Do Not Track": "This question identifies whether the service may ignore 'Do Not Track' header requests. You can learn more about the 'Do Not Track' policy <a href='https://www.eff.org/issues/do-not-track'>here</a>.",
    "Identification": "This question identifies whether the service collects your IP address or device ID, which can be used to uniquely identify you.",
    "Policy Change": "The question identifies whether the service can update the privacy policy without notifying you.",
    "Retention": "This question identifies whether the service deletes your data after you delete your account.",
    "Security": "The question identifies if the service encrypts your data. Read more about encryption <a href='https://ssd.eff.org/en/module/what-encryption'>here</a>.",
    "Social Media": "This question identifies if the service can access your social media profiles. If you have chosen to connect to this service through your social media account, it may augment information collected about you with data from your social media sites.",
    "Targeted Advertising": "This question identifies if the service uniquely targets you in their advertising.",
    "Analysis": "This question identifies whether the service performs statistical or demographic analysis of data it collects about you. This analysis may be anonymized and aggregated.",
    "Collection": "This question identifies if the service collects generic or identifiable information about you.",
    "3P Sharing": "This question identifies whether your information can be shared with third parties. You can learn more about data sharing with third party advertisers <a href='https://www.eff.org/deeplinks/2009/09/online-trackers-and-social-networks'>here</a>.",
    "Location": "This question identifies whether the service tracks your physical location.",
    "Contact Info": "This question identifies whether the service collects contact information, such as your email, phone number, or mailing address.",
    "Personalization": "This question identifies whether the service can use your data to customize the content you see.",
    "Payment": "This question identifies whether the service can collect your payment information.",
    }

    return dim_to_question_desc[dim]