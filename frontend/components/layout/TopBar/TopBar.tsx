type Props = {
  children?: React.ReactNode;
};

export default function TopBar({ children }: Props) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 bg-white px-6">
      <p className="text-sm text-slate-400">AI Health System Gateway</p>
      {children && <div className="flex items-center gap-3">{children}</div>}
    </header>
  );
}
