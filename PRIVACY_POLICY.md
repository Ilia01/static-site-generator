# Privacy Policy

**Last Updated:** October 2025

ApiFlow ("we", "us", or "our") is committed to protecting your privacy. This Privacy Policy explains what information we collect, how we use it, and your rights.

---

## TL;DR (Summary)

**We collect almost nothing:**
- ✅ License validation happens **offline** (no phone-home)
- ✅ No analytics or tracking
- ✅ No telemetry or usage data
- ✅ Your API specs stay on your machine
- ✅ Generated docs stay on your machine
- ❌ We don't know what APIs you're documenting
- ❌ We don't track how often you use ApiFlow

**We only collect:**
- Purchase email (from payment processor - Gumroad)
- Support emails (if you contact us)
- That's it.

---

## 1. Information We Collect

### 1.1 Information You Provide

**Purchase Information:**
When you buy a PRO or BUSINESS license:
- Email address (collected by Gumroad, shared with us for license delivery)
- Payment information (processed by Gumroad, we never see card details)
- Order ID (from Gumroad)
- License tier purchased (PRO or BUSINESS)

**Support Communications:**
If you contact us for support:
- Email address
- Name (optional)
- Technical details you choose to share
- Screenshots or files you send (optional)

**That's it.** We don't collect anything else.

### 1.2 Information We DON'T Collect

We do NOT collect:
- ❌ Analytics or usage tracking
- ❌ Telemetry data
- ❌ Your API specifications
- ❌ Generated documentation content
- ❌ IP addresses or device information
- ❌ Browsing history
- ❌ Location data
- ❌ How often you use ApiFlow
- ❌ What APIs you're documenting
- ❌ Error reports (unless you manually send them)

**ApiFlow is a local tool.** Everything happens on your machine.

---

## 2. How We Use Information

### 2.1 Purchase Information

We use your email to:
- ✅ Deliver your license key
- ✅ Send order confirmation
- ✅ Provide purchase receipt
- ✅ Respond to refund requests

We do NOT use your email to:
- ❌ Send marketing emails (unless you opt in)
- ❌ Sell to third parties
- ❌ Spam you with promotions

### 2.2 Support Information

We use support communications to:
- ✅ Answer your questions
- ✅ Fix bugs you report
- ✅ Improve documentation
- ✅ Provide technical assistance

---

## 3. License Validation

### 3.1 Offline Validation

License keys are validated **completely offline**:

1. You set license key via environment variable or config file
2. ApiFlow validates the key **locally** (on your machine)
3. Validation result is cached in `.apiflow/` directory (local cache)
4. **No internet connection required**
5. **No data sent to our servers**

**Privacy-First Design:**
- No phone-home
- No tracking
- No analytics
- Validation happens on your computer only

### 3.2 What's in the License Cache

The `.apiflow/` directory stores:
- License validation result (valid/invalid)
- License tier (FREE/PRO/BUSINESS)
- Validation timestamp

**Does NOT store:**
- Your API specs
- Generated documentation
- Personal information
- Usage statistics

**Location:** `.apiflow/` in your home directory or project root

---

## 4. Data Storage and Security

### 4.1 Where Data is Stored

**Purchase Data:**
- Stored by Gumroad (our payment processor)
- Email addresses stored in our support system (if you contact us)
- All data stored securely with encryption

**Local Data:**
- License cache stored on your computer (`.apiflow/` directory)
- Your API specs never leave your machine
- Generated docs stay on your machine

### 4.2 Security Measures

We implement reasonable security measures:
- ✅ Encrypted email communication
- ✅ Secure payment processing (via Gumroad)
- ✅ No storage of sensitive data
- ✅ Minimal data collection

**However:** No system is 100% secure. We cannot guarantee absolute security.

---

## 5. Third-Party Services

### 5.1 Payment Processing

We use **Gumroad** for payment processing:
- Gumroad collects payment information
- Gumroad's privacy policy applies: https://gumroad.com/privacy
- We receive only: email, order ID, product purchased
- We never see credit card details

### 5.2 Email Hosting

Support emails may be hosted by:
- Gmail / Google Workspace
- Other email providers
- Subject to their privacy policies

### 5.3 No Analytics Services

We do NOT use:
- ❌ Google Analytics
- ❌ Mixpanel, Amplitude, etc.
- ❌ Error tracking services (Sentry, etc.)
- ❌ Any third-party analytics

**Your usage is private.**

---

## 6. Data Retention

### 6.1 How Long We Keep Data

**Purchase Information:**
- Retained for 7 years (for tax/legal compliance)
- Email address kept indefinitely (for license support)
- You can request deletion (see "Your Rights" below)

**Support Communications:**
- Retained as long as relevant for support
- Typically 1-2 years after last contact
- You can request deletion

**Local Cache:**
- Stored on your machine indefinitely
- You can delete `.apiflow/` directory anytime
- No data sent to us

### 6.2 Data Deletion

You can request data deletion by emailing support@yourdomain.com:
- We'll delete your email and purchase info
- License key will be revoked (no refund)
- Local cache unaffected (it's on your machine)

---

## 7. Your Rights

### 7.1 Right to Access

You can request:
- Copy of personal data we have about you
- Confirmation of what data we store
- Details on how we use your data

**How:** Email support@yourdomain.com

### 7.2 Right to Deletion

You can request deletion of:
- Your email address
- Purchase history (after legal retention period)
- Support communications

**Note:** Deletion may result in inability to provide support or deliver license keys.

### 7.3 Right to Correction

If we have incorrect information:
- Contact us to correct it
- We'll update our records promptly

### 7.4 Right to Object

You can object to:
- Marketing emails (we send very few)
- Data processing (but this may affect our ability to provide service)

### 7.5 Right to Portability

You can request:
- Copy of your data in machine-readable format
- Transfer to another service (if applicable)

---

## 8. Children's Privacy

ApiFlow is not intended for children under 13:
- We don't knowingly collect data from children
- If we learn we have child data, we'll delete it
- Parents/guardians can contact us to request deletion

---

## 9. International Users

### 9.1 Data Transfers

ApiFlow is used worldwide:
- Your data may be stored in [Your Country]
- Gumroad may store data in their locations
- By using ApiFlow, you consent to international data transfer

### 9.2 GDPR Compliance (EU Users)

If you're in the EU:
- We comply with GDPR
- You have all rights listed in "Your Rights" section
- Data processing is lawful (contract performance, legitimate interest)
- You can file complaints with your data protection authority

### 9.3 CCPA Compliance (California Users)

If you're in California:
- You have rights under CCPA
- We don't sell personal information
- You can request disclosure of data collected
- You can request deletion

---

## 10. Cookies and Tracking

### 10.1 No Cookies in Software

ApiFlow software does NOT use cookies:
- No web-based tracking
- No browser cookies
- No persistent identifiers

### 10.2 Website/Landing Page

If we have a website (separate from this repository):
- May use essential cookies (for functionality)
- Will disclose in website's cookie policy
- Will provide cookie consent banner (if required)

**This policy covers ApiFlow software, not our website.**

---

## 11. Open Source Considerations

### 11.1 Public Repository

ApiFlow source code is public on GitHub:
- Don't include personal data in bug reports
- Don't share license keys in issues/discussions
- Screenshots should redact sensitive information

### 11.2 Community Contributions

If you contribute code:
- Your GitHub username may be public
- Commit messages/comments are public
- Follow GitHub's privacy policy

---

## 12. Changes to Privacy Policy

### 12.1 Updates

We may update this policy:
- Changes posted to GitHub repository
- "Last Updated" date will change
- Significant changes announced via GitHub releases
- Continued use = acceptance of changes

### 12.2 Notification

For material changes:
- Announce in GitHub releases
- Email notification (if we have your email)
- 30-day notice when possible

---

## 13. Data Breaches

### 13.1 Our Commitment

If a data breach occurs:
- We'll investigate immediately
- Notify affected users within 72 hours
- Provide details of what data was affected
- Explain steps we're taking

### 13.2 Minimize Risk

We minimize breach risk by:
- Collecting minimal data
- Not storing sensitive information
- Using secure third-party services
- Offline license validation

---

## 14. Business Transfers

If ApiFlow is sold or merged:
- Your data may transfer to new owner
- New owner must honor this policy
- We'll notify you of ownership change
- You can request deletion before transfer

---

## 15. Legal Disclosures

We may disclose information if required by:
- Law enforcement (with valid legal request)
- Court order or subpoena
- Legal obligation
- Protection of our rights or safety

**We'll notify you unless legally prohibited.**

---

## 16. Contact Us

Questions about privacy?

**Email:** support@yourdomain.com
**GitHub Issues:** https://github.com/Ilia01/apiflow/issues
**Mail:** [Your mailing address if required]

**Response Time:** Within 30 days of request (GDPR/CCPA compliance)

---

## 17. Summary of Key Points

| What | Details |
|------|---------|
| **What we collect** | Email (for license delivery), support emails |
| **What we DON'T collect** | Analytics, telemetry, usage tracking, API specs |
| **License validation** | 100% offline (no phone-home) |
| **Third parties** | Gumroad (payments only) |
| **Your rights** | Access, deletion, correction, portability |
| **Data retention** | 7 years (legal), or until you request deletion |
| **International** | GDPR compliant (EU), CCPA compliant (CA) |
| **Children** | Not for under 13 |
| **Contact** | support@yourdomain.com |

---

## 18. Accountability

**Responsible Party:**
- ApiFlow / [Your legal entity name]
- [Your address if required]
- support@yourdomain.com

**Data Protection Officer (if required):**
- [Name if you have one]
- [Email if applicable]

---

## Our Promise

**We built ApiFlow with privacy in mind:**
- No tracking
- No analytics
- No phone-home
- Your data stays yours

**We only know you exist if:**
1. You buy a license (Gumroad tells us)
2. You email us for support

**That's it.** Use ApiFlow in peace.

---

**Questions?** Email support@yourdomain.com
