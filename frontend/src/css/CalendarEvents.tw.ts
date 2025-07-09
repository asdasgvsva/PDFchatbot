// CalendarEvents.tw.ts

export const section = 'w-full bg-white rounded-2xl shadow-md p-5 mb-4';
export const dot = 'text-red-500 text-xs ml-1';
export const loading = 'text-gray-500 text-sm mt-2';
export const error = 'text-red-500 text-sm mt-2';
export const table = 'mt-3 w-full border-collapse';
export const th = 'border-b border-gray-300 text-left p-1 text-sm font-semibold';
export const td = 'p-1 max-w-[120px] min-w-[60px] truncate text-sm';
export const tr = (idx: number, len: number) => idx !== len - 1 ? 'border-b border-gray-100' : '';
export const moreIndicator = 'text-gray-400 text-xs mt-1 text-center';
export const tableWrapper = 'max-h-[400px] overflow-y-auto';
export const tbody = 'block max-h-[350px] overflow-y-auto w-full';
