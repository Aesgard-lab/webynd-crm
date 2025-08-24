import * as React from "react";

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"];

export default function BillingChart({
  bars = [1, 0.6, 0.7, 0.6, 0.9, 1, 0.4],
  title = "Monthly Billing",
}: { bars?: number[]; title?: string }) {
  return (
    <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#dbe0e6] p-6">
      <p className="text-base font-medium text-gray-900">{title}</p>
      <div className="grid min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
        {bars.map((v, i) => (
          <React.Fragment key={i}>
            <div
              className="w-full border-t-2 border-[#60758a] bg-[#f0f2f5]"
              style={{ height: `${Math.round(v * 100)}%` }}
            />
            <p className="text-[13px] font-bold leading-normal tracking-[0.015em] text-[#60758a]">
              {MONTHS[i] ?? ""}
            </p>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
