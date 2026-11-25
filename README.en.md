# ARANDU TAPE

[Português](README.md)

**Experimental adaptive graphical navigation for Linux, focused on accessibility, human autonomy and meaningful learning.**

ARANDU TAPE explores a central Seed and three visual Rivers: Memory (recent items), Open (session windows), and Frequent (frequently used applications). Medallions provide navigation targets. The project aims to reveal complexity on demand, preserve task continuity and allow accessible, reversible interaction.

## Current scope

| Component | Code identifier | Scope |
| --- | --- | --- |
| Confluência / GNOME Suite | 3.2.3-beta | GNOME Shell extension and GTK3 companion |
| TOPBAR | 6.6.1.2; experimental variant 6613 | Panel identity |
| ARANDU Desktop | 0.7.7 | GTK4 prototype and optional Sway lab |
| Confluência installer | 2.8.2 (legacy identifier) | User-profile installation |

These identifiers are independent. The project is not a stable Linux distribution, a new compositor, or a clinically validated assistive technology. Linux Mint with GNOME 46/X11 is the historical test environment; real compatibility must be validated for the candidate. Sway is a third-party compositor used by an optional lab.

## Getting started

Use a Git clone for complete contract tests and snapshot screening. Read the [GNOME installation guide](INSTALAR.md) or [GTK4 manual](ARANDU-DESKTOP/README.md) before running anything. Do not run the user-profile installer with sudo. Keep a working desktop session and backups. The [nested Sway lab](ARANDU-DESKTOP/session/README.md) is optional; do not make it your default login before testing recovery.

Most detailed manuals are currently in Portuguese. See the [documentation index](docs/README.md), [version evidence](docs/ESTADO_E_VERSOES.md), [Design Core](docs/DESIGN_CORE.md) and [accessibility guide](docs/ACESSIBILIDADE.md).

## Research, privacy and citation

Meaningful learning theory informs design hypotheses, not a claim of proven machine cognition or user learning. The public graphical environment should function without private experimental research cores. See the [public foundations](docs/FUNDAMENTACAO_PUBLICA.md).

History in the GNOME/GTK3 component is stored locally according to the current privacy controls. Optional external AI requests send explicitly entered text to the chosen provider. Read [privacy](docs/PRIVACIDADE.md) and [security](SECURITY.md).

Citation metadata is available in [CITATION.cff](CITATION.cff). Cite the exact Git commit until an archived release DOI has been confirmed. No scientific release or DOI has been confirmed at this stage. Public source visibility does not establish an open-source license: ownership, provenance, licensing and release approval remain under review. See the [publication policy](docs/PUBLICACAO_CIENTIFICA_ZENODO.md) and [contribution guide](CONTRIBUTING.md).

> Technology that adapts to human possibilities.
