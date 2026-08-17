import React, { useState, useMemo, useEffect, useRef } from "react";
import {
  LayoutDashboard, TrendingUp, Truck, CloudRain, Package, ShoppingCart, Bell,
  FileText, Settings as SettingsIcon, Menu, X, Sun, Moon, MapPin, AlertTriangle,
  CheckCircle2, Info, Download, Printer, RefreshCw, ArrowUp, ArrowDown, Sprout,
  Warehouse, Calendar, ChevronRight, ChevronDown, Gauge, Search, BarChart3,
  Wallet, Fuel, Users, Boxes, ShieldAlert, ShieldCheck, Clock, Building2,
  ClipboardList, Percent, Droplets, Thermometer, Wind, ChevronLeft,
  MessageCircle, Sparkles, Send
} from "lucide-react";
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  RadialBarChart, RadialBar, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip,
  Legend, ResponsiveContainer, ComposedChart
} from "recharts";
import * as XLSX from "xlsx";

/* ============================================================
   DESIGN TOKENS
   A government agri-market intelligence portal. Blue = trust /
   institutional authority. Green = agriculture / growth. A thin
   tricolour rule under the header nods to the Indian-government
   context (saffron / navy / green) without being kitsch, and a
   circular "seal" mark stands in for an official emblem.
   ============================================================ */
const PALETTE = {
  light: {
    bg: "#EEF3F8", surface: "#FFFFFF", surfaceAlt: "#F5F9FC",
    ink: "#0F1E33", inkSoft: "#5B6E85", inkFaint: "#8DA0B5",
    border: "#DCE6EF", borderSoft: "#E9F0F6",
    primary: "#0B5FA5", primaryDeep: "#08477E", primarySoft: "#E5EFF9",
    green: "#0E9D6E", greenSoft: "#E1F6EE", greenDeep: "#087551",
    shadow: "0 1px 2px rgba(15,30,51,0.04), 0 10px 30px rgba(15,30,51,0.07)"
  },
  dark: {
    bg: "#08111F", surface: "#0F1C2E", surfaceAlt: "#0B1626",
    ink: "#E8F1FA", inkSoft: "#93A8C0", inkFaint: "#5D7089",
    border: "#1D2C42", borderSoft: "#162335",
    primary: "#5AA9E6", primaryDeep: "#8CC5F0", primarySoft: "#122844",
    green: "#3FD6A3", greenSoft: "#0E2A22", greenDeep: "#6EE7BE",
    shadow: "0 1px 2px rgba(0,0,0,0.4), 0 10px 30px rgba(0,0,0,0.45)"
  }
};
const RISK = {
  safe: { key: "safe", label: "Normal", c: "#16A34A", bgL: "#E7F7ED", bgD: "#0E2A1C" },
  watch: { key: "watch", label: "Watch", c: "#D97706", bgL: "#FDF1DE", bgD: "#2E2109" },
  spike: { key: "spike", label: "Price Spike Expected", c: "#EA580C", bgL: "#FDE9DD", bgD: "#331C0C" },
  critical: { key: "critical", label: "Immediate Intervention Required", c: "#DC2626", bgL: "#FCE4E4", bgD: "#330F0F" }
};
const FONT_LINK = "https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap";

/* ============================================================
   MOCK REFERENCE DATA
   ============================================================ */
const COMMODITIES = ["Onion", "Tomato", "Wheat", "Rice (Paddy)", "Potato", "Tur Dal (Arhar)", "Soybean", "Sugarcane"];
const STATE_DISTRICTS = {
  Maharashtra: ["Nashik", "Pune", "Ahmednagar", "Solapur"],
  "Uttar Pradesh": ["Agra", "Lucknow", "Kanpur", "Meerut"],
  "Madhya Pradesh": ["Indore", "Bhopal", "Ujjain", "Mandsaur"],
  Karnataka: ["Bengaluru Rural", "Hubballi", "Belagavi", "Kolar"],
  Punjab: ["Ludhiana", "Amritsar", "Patiala", "Bathinda"],
  Gujarat: ["Rajkot", "Ahmedabad", "Surat", "Bhavnagar"],
  Rajasthan: ["Jaipur", "Kota", "Alwar", "Sri Ganganagar"],
  "West Bengal": ["Bardhaman", "Hooghly", "Nadia", "Malda"],
  Bihar: ["Patna", "Muzaffarpur", "Gaya", "Bhagalpur"],
  "Tamil Nadu": ["Coimbatore", "Salem", "Madurai", "Erode"]
};
const STATES = Object.keys(STATE_DISTRICTS);
const MARKETS = ["Main Mandi", "APMC Yard", "Wholesale Market", "Regulated Market Committee"];

export default function App() {
  const [dark, setDark] = useState(false);
  const t = dark ? PALETTE.dark : PALETTE.light;

  return (
    <div style={{ background: t.bg, minHeight: "100vh", fontFamily: "Inter, sans-serif" }}>
      <div className="p-8 text-center">
        <h1 style={{ color: t.ink }}>🎨 Jugraj's Price Intelligence UI</h1>
        <p style={{ color: t.inkSoft }}>React Dashboard Component Loaded Successfully!</p>
      </div>
    </div>
  );
}
