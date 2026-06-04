export default function HomeStepCard({ step, title, description }) {
  return (
    <div className="relative p-6 bg-gray-50 rounded-xl border border-gray-200">
      <div className="absolute -top-4 -left-4 w-10 h-10 bg-blue-600 text-white font-bold rounded-full flex items-center justify-center border-4 border-white">
        {step}
      </div>
      <h4 className="text-lg font-bold text-gray-800 mt-2 mb-2">{title}</h4>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}