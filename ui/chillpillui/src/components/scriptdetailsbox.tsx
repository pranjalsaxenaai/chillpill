"use client"

type ScriptDetailsBoxProps = {
    scriptContent: string;
};

const ScriptDetailsBox: React.FC<ScriptDetailsBoxProps> = ({scriptContent}) => {
    return (
        <details className="mb-4 bg-white rounded-lg shadow-sm">
        <summary className="px-4 py-3 font-semibold cursor-pointer select-none">
          Script
        </summary>
        <div className="p-4">
          <textarea
            /*Show Script Content */
            value={scriptContent}
            className="w-full min-h-[60px] mb-3 rounded border border-gray-300 p-2"
            readOnly
          />
        </div>
      </details>
    );
};

export default ScriptDetailsBox;