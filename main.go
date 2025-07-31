package main

import (
	"fmt"
	"os"
	"runtime"
	"time"

	"github.com/awesome-project/go-multi-platform/cmd"
	"github.com/awesome-project/go-multi-platform/internal/platform"
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	version = "1.0.0"
	commit  = "development"
	date    = "unknown"
)

func main() {
	// Initialize platform detection
	platform.Init()

	// Create root command
	rootCmd := &cobra.Command{
		Use:     "go-multi-platform",
		Short:   "🚀 Advanced Multi-Platform Go Application",
		Long:    `An impressive Go application designed to work seamlessly on Kali Linux and Termux with advanced features and beautiful UI.`,
		Version: fmt.Sprintf("%s (commit: %s, built: %s)", version, commit, date),
		PersistentPreRun: func(cmd *cobra.Command, args []string) {
			// Show startup banner
			showBanner()
		},
	}

	// Add subcommands
	cmd.AddCommands(rootCmd)

	// Execute
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func showBanner() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)
	blue := color.New(color.FgBlue, color.Bold)

	fmt.Println()
	cyan.Println("╔══════════════════════════════════════════════════════════════╗")
	cyan.Println("║                    🚀 GO MULTI-PLATFORM 🚀                  ║")
	cyan.Println("║                                                              ║")
	cyan.Println("║  Advanced Go Application for Kali Linux & Termux            ║")
	cyan.Println("║  Version:", version, "                                    ║")
	cyan.Println("╚══════════════════════════════════════════════════════════════╝")
	fmt.Println()

	// Platform info
	platformInfo := platform.GetPlatformInfo()
	green.Printf("📍 Platform: %s\n", platformInfo.Name)
	yellow.Printf("🖥️  OS: %s %s\n", platformInfo.OS, platformInfo.Arch)
	blue.Printf("🐧 Kernel: %s\n", platformInfo.Kernel)
	red.Printf("⚡ Go Version: %s\n", runtime.Version())
	fmt.Println()

	// Show current time
	timeStr := time.Now().Format("2006-01-02 15:04:05")
	cyan.Printf("🕐 Started at: %s\n", timeStr)
	fmt.Println()
}