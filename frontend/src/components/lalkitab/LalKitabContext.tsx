import { createContext, useContext, useState, type ReactNode } from 'react';

interface LalKitabContextValue {
  kundliId: string | null;
  chartData: any;
  birthDate: string | null;
  apiResult: any;
  fullData: any;  // from consolidated /api/lalkitab/full/{id} endpoint
  setKundliId: (id: string | null) => void;
  setChartData: (data: any) => void;
  setBirthDate: (date: string | null) => void;
  setApiResult: (data: any) => void;
  setFullData: (data: any) => void;
}

const LalKitabContext = createContext<LalKitabContextValue | null>(null);

export function LalKitabProvider({ children }: { children: ReactNode }) {
  const [kundliId, setKundliId] = useState<string | null>(null);
  const [chartData, setChartData] = useState<any>(null);
  const [birthDate, setBirthDate] = useState<string | null>(null);
  const [apiResult, setApiResult] = useState<any>(null);
  const [fullData, setFullData] = useState<any>(null);

  return (
    <LalKitabContext.Provider value={{
      kundliId, chartData, birthDate, apiResult, fullData,
      setKundliId, setChartData, setBirthDate, setApiResult, setFullData,
    }}>
      {children}
    </LalKitabContext.Provider>
  );
}

export function useLalKitab() {
  const ctx = useContext(LalKitabContext);
  if (!ctx) throw new Error('useLalKitab must be used within LalKitabProvider');
  return ctx;
}
