export default function Footer() {
  return (
    <footer className="w-full bg-gray-800 text-gray-200 py-4 mt-8 flex flex-col md:flex-row items-center justify-between px-6">
      <p className="text-sm">Made with 💗 by Exovision &copy; {new Date().getFullYear()}</p>
      <div className="flex gap-4 mt-2 md:mt-0">
        <a
          href="https://github.com/PPilot2/exovision"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-white"
        >
          GitHub
        </a>
      </div>
    </footer>
  );
}
