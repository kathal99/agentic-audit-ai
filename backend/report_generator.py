import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class AuditReportCompiler:
    @staticmethod
    def generate_markdown(transcript: list[dict], patches: list[dict], final_score: int) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        md = f"""# AGENTIC AUDIT AI // COMPLIANCE & SECURITY REPORT
**Operator:** katelynn@kalib
**Final Security Score:** {final_score}/100
**Timestamp:** {timestamp}
---
## 1. EXECUTIVE SUMMARY
* **Total adversarial rounds:** {len([t for t in transcript if t.get('agent') == 'chaos'])}
* **Intercepted exploits (DENY):** {len([t for t in transcript if t.get('action') == 'DENY'])}
* **PII/secret leak vectors blocked:** {len([t for t in transcript if t.get('pii_detected')])}
* **Dynamic ChromaDB patches applied:** {len(patches)}
---
## 2. TRANSCRIPT LOGS
"""
        for entry in transcript:
            agent = entry.get("agent", "UNKNOWN").upper()
            round_num = entry.get("round", 0)
            text = entry.get("text", "")
            action = entry.get("action")
            entropy = entry.get("entropy")
            md += f"\n### [Round {round_num}] Agent: {agent}\n"
            if action:
                md += f"**Verdict:** `{action}`\n"
            if entropy is not None:
                md += f"**Entropy:** `{entropy}`\n"
            md += f"```text\n{text}\n```\n"
        md += "\n---\n\n## 3. APPLIED VECTOR PATCHES\n"
        if not patches:
            md += "No automated vector patches were deployed during this audit cycle.\n"
        else:
            for idx, p in enumerate(patches, 1):
                md += f"{idx}. `{p.get('patch', '')}`\n"
        return md

    @staticmethod
    def generate_pdf(transcript: list[dict], patches: list[dict], final_score: int, output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor('#00f0ff'),
            spaceAfter=12,
        )
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#e0e6ed'),
            spaceAfter=8,
        )
        elements = [
            Paragraph("AGENTIC AUDIT AI // SECURITY & COMPLIANCE CERTIFICATE", title_style),
            Paragraph(f"<b>Operator:</b> katelynn@kalib", body_style),
            Paragraph(f"<b>Final Security Score:</b> {final_score}/100", body_style),
            Paragraph(f"<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", body_style),
            Spacer(1, 12),
        ]
        for entry in transcript:
            text = entry.get("text", "")
            agent = entry.get("agent", "UNKNOWN").upper()
            round_num = entry.get("round", 0)
            action = entry.get("action")
            entropy = entry.get("entropy")
            lines = [
                Paragraph(f"<b>[{agent}] Round {round_num}</b>", body_style),
                Paragraph(f"<b>Verdict:</b> {action or 'N/A'}", body_style),
                Paragraph(f"<b>Entropy:</b> {entropy if entropy is not None else 'N/A'}", body_style),
                Paragraph(f"<pre>{text}</pre>", body_style),
                Spacer(1, 8),
            ]
            elements.extend(lines)
        if patches:
            elements.append(Paragraph("<b>Applied Vector Patches</b>", body_style))
            for patch in patches:
                elements.append(Paragraph(f"- {patch.get('patch', '')}", body_style))
        doc.build(elements)
        return output_path
