# blendPilot - AI-Assisted 3D Modeling for 3D Printing

Precision 3D modeling and additive manufacturing (FDM / Resin) environment driven by **Blender** using the **Model Context Protocol (MCP)**.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 📖 Overview

**blendPilot** provides a technical and reproducible methodology for designing functional 3D printable parts (not just prototypes) using Blender and AI agents. Every piece is parametrically engineered with strict adherence to physical dimensions, strict clearance tolerances, watertight manifold geometry, and 3D printing constraints.

---

## 📁 Repository Structure

```text
blendPilot/
├── GEMINI.md            # Modeling methodology, engineering rules & guidelines
├── README.md            # Project documentation and setup guide
├── LICENSE              # CC BY-NC 4.0 Non-Commercial License
├── scripts/             # Fully reproducible parametric Python (bpy) scripts
├── out/                 # Generated 3D models (.stl) and multi-angle renders (.png)
├── specs/               # Official dimension sheets, datasheets & caliper measurements
└── tools/
    └── blender-mcp/     # MCP bridge between AI agents and Blender
```

---

## 🚀 How It Works

1. **Start Blender**:
   - Open Blender 4.2+ LTS.
   - In the 3D Viewport sidebar (press **N**), navigate to the **BlenderMCP** tab and click **Connect**.
2. **AI-Driven Modeling**:
   - Provide a design request (e.g. *"Design a phone case for Huawei P30"*).
   - Dimension specs and datasheets are verified in `specs/`.
   - A clean, parametric Python script is generated in `scripts/`.
   - The script runs directly inside Blender via the MCP server.
   - Geometry is validated (watertight/manifold, zero non-manifold edges, minimum wall thickness).
   - Final deliverables (`.stl` models and multi-angle inspection `.png` renders) are saved into `out/`.

---

## 📄 License & Attribution

This project is licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

- **Non-Commercial**: You may not use this material for commercial purposes without explicit permission.
- **Attribution**: You must give appropriate credit to **IB2M-Official**, provide a link to the license, and indicate if changes were made.
- For commercial licensing inquiries or official partnerships, contact **IB2M-Official**.
