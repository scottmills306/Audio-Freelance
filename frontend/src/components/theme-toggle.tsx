"use client";

import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  if (!mounted) return <div className="h-6" />;

  const toggle = () => {
    const html = document.documentElement;
    const isDark = html.classList.contains("dark");
    html.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "light" : "dark");
  };

  return (
    <div className="flex items-center justify-between text-xs">
      <button
        onClick={toggle}
        className="px-2 py-1 rounded hover:bg-accent transition-colors cursor-pointer"
        title="Toggle theme"
      >
        <span className="text-sm">☀</span> / <span className="text-sm">☾</span>
      </button>
      <span className="text-muted-foreground">Theme</span>
    </div>
  );
}
