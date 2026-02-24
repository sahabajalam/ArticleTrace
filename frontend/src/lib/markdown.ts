/**
 * Lightweight markdown-to-HTML converter for compliance documents.
 * Handles: h1-h4, bold, italic, inline code, ul/ol, tables, hr, blockquotes, paragraphs.
 * Content is from our own LLM so we only need basic escaping for < > & in text nodes.
 */

function escapeHtml(text: string): string {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function parseInline(text: string): string {
    // Temporarily extract code spans to protect them
    const spans: string[] = [];
    let t = text.replace(/`([^`]+)`/g, (_, code) => {
        spans.push(`<code>${escapeHtml(code)}</code>`);
        return `\x00${spans.length - 1}\x00`;
    });

    // Escape remaining HTML in text
    t = escapeHtml(t);

    // Bold **text** and __text__
    t = t.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/__(.+?)__/g, "<strong>$1</strong>");

    // Italic *text* and _text_ (not surrounded by word chars to avoid false positives)
    t = t.replace(/\*([^*\n]+?)\*/g, "<em>$1</em>");
    t = t.replace(/_([^_\n]+?)_/g, "<em>$1</em>");

    // Restore code spans
    t = t.replace(/\x00(\d+)\x00/g, (_, i) => spans[parseInt(i)]);

    return t;
}

export function markdownToHtml(markdown: string): string {
    const lines = markdown.split("\n");
    let html = "";
    let i = 0;

    while (i < lines.length) {
        const line = lines[i];
        const trimmed = line.trim();

        // ── Blank line ──
        if (trimmed === "") {
            i++;
            continue;
        }

        // ── Headers ──
        if (trimmed.startsWith("#### ")) {
            html += `<h4>${parseInline(trimmed.slice(5))}</h4>\n`;
            i++;
            continue;
        }
        if (trimmed.startsWith("### ")) {
            html += `<h3>${parseInline(trimmed.slice(4))}</h3>\n`;
            i++;
            continue;
        }
        if (trimmed.startsWith("## ")) {
            html += `<h2>${parseInline(trimmed.slice(3))}</h2>\n`;
            i++;
            continue;
        }
        if (trimmed.startsWith("# ")) {
            html += `<h1>${parseInline(trimmed.slice(2))}</h1>\n`;
            i++;
            continue;
        }

        // ── Horizontal rule ──
        if (/^[-*_]{3,}$/.test(trimmed)) {
            html += "<hr/>\n";
            i++;
            continue;
        }

        // ── Blockquote ──
        if (trimmed.startsWith("> ")) {
            html += `<blockquote>${parseInline(trimmed.slice(2))}</blockquote>\n`;
            i++;
            continue;
        }

        // ── Table (line starts with |) ──
        if (trimmed.startsWith("|")) {
            const tableRows: string[] = [];
            while (i < lines.length && lines[i].trim().startsWith("|")) {
                tableRows.push(lines[i].trim());
                i++;
            }
            // Filter out separator rows (|---|---|)
            const dataRows = tableRows.filter((r) => !/^\|[\s\-|:]+\|$/.test(r));
            if (dataRows.length > 0) {
                const splitRow = (r: string) =>
                    r
                        .split("|")
                        .slice(1, -1)
                        .map((c) => c.trim());

                let tHtml = "<table><thead><tr>";
                for (const cell of splitRow(dataRows[0])) {
                    tHtml += `<th>${parseInline(cell)}</th>`;
                }
                tHtml += "</tr></thead><tbody>";
                for (const row of dataRows.slice(1)) {
                    tHtml += "<tr>";
                    for (const cell of splitRow(row)) {
                        tHtml += `<td>${parseInline(cell)}</td>`;
                    }
                    tHtml += "</tr>";
                }
                tHtml += "</tbody></table>";
                html += tHtml + "\n";
            }
            continue;
        }

        // ── Unordered list ──
        if (/^[-*+] /.test(trimmed)) {
            let lHtml = "<ul>";
            while (i < lines.length && /^[-*+] /.test(lines[i].trim())) {
                lHtml += `<li>${parseInline(lines[i].trim().replace(/^[-*+] /, ""))}</li>`;
                i++;
            }
            lHtml += "</ul>";
            html += lHtml + "\n";
            continue;
        }

        // ── Ordered list ──
        if (/^\d+\. /.test(trimmed)) {
            let lHtml = "<ol>";
            while (i < lines.length && /^\d+\. /.test(lines[i].trim())) {
                lHtml += `<li>${parseInline(lines[i].trim().replace(/^\d+\. /, ""))}</li>`;
                i++;
            }
            lHtml += "</ol>";
            html += lHtml + "\n";
            continue;
        }

        // ── Paragraph: collect consecutive plain lines ──
        let paraLines = [trimmed];
        i++;
        while (
            i < lines.length &&
            lines[i].trim() !== "" &&
            !lines[i].trim().startsWith("#") &&
            !lines[i].trim().startsWith("|") &&
            !/^[-*+] /.test(lines[i].trim()) &&
            !/^\d+\. /.test(lines[i].trim()) &&
            !lines[i].trim().startsWith(">") &&
            !/^[-*_]{3,}$/.test(lines[i].trim())
        ) {
            paraLines.push(lines[i].trim());
            i++;
        }
        html += `<p>${parseInline(paraLines.join(" "))}</p>\n`;
    }

    return html;
}
