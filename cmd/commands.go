package cmd

import (
	"fmt"

	"github.com/awesome-project/go-multi-platform/internal/platform"
	"github.com/awesome-project/go-multi-platform/internal/features"
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

func AddCommands(rootCmd *cobra.Command) {
	// System info command
	rootCmd.AddCommand(systemCmd)
	
	// Network tools command
	rootCmd.AddCommand(networkCmd)
	
	// Security tools command
	rootCmd.AddCommand(securityCmd)
	
	// Installation command
	rootCmd.AddCommand(installCmd)
	
	// Demo command
	rootCmd.AddCommand(demoCmd)
	
	// Platform-specific commands
	if platform.GetPlatformInfo().IsKali {
		rootCmd.AddCommand(kaliCmd)
	} else if platform.GetPlatformInfo().IsTermux {
		rootCmd.AddCommand(termuxCmd)
	}
}

var systemCmd = &cobra.Command{
	Use:   "system",
	Short: "🔍 System Information and Analysis",
	Long:  `Display comprehensive system information, performance metrics, and platform-specific details.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.ShowSystemInfo()
	},
}

var networkCmd = &cobra.Command{
	Use:   "network",
	Short: "🌐 Network Analysis and Tools",
	Long:  `Advanced network scanning, analysis, and monitoring tools optimized for your platform.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.ShowNetworkTools()
	},
}

var securityCmd = &cobra.Command{
	Use:   "security",
	Short: "🔒 Security Analysis and Testing",
	Long:  `Security assessment tools, vulnerability scanning, and penetration testing capabilities.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.ShowSecurityTools()
	},
}

var installCmd = &cobra.Command{
	Use:   "install",
	Short: "📦 Installation Instructions",
	Long:  `Get platform-specific installation instructions and setup guide.`,
	Run: func(cmd *cobra.Command, args []string) {
		cyan := color.New(color.FgCyan, color.Bold)
		green := color.New(color.FgGreen, color.Bold)
		
		cyan.Println("📦 Installation Guide")
		fmt.Println()
		
		instructions := platform.GetInstallationInstructions()
		green.Println(instructions)
		fmt.Println()
		
		platform.ShowPlatformFeatures()
	},
}

var demoCmd = &cobra.Command{
	Use:   "demo",
	Short: "🎮 Interactive Demo Mode",
	Long:  `Experience an interactive demonstration of all features with beautiful animations.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.RunDemo()
	},
}

var kaliCmd = &cobra.Command{
	Use:   "kali",
	Short: "⚔️ Kali Linux Specific Tools",
	Long:  `Advanced penetration testing and security analysis tools exclusive to Kali Linux.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.ShowKaliTools()
		platform.ShowKaliToolsStatus()
		platform.ShowKaliAdvancedFeatures()
	},
}

var termuxCmd = &cobra.Command{
	Use:   "termux",
	Short: "📱 Termux Specific Features",
	Long:  `Mobile-optimized tools and features designed specifically for Termux on Android.`,
	Run: func(cmd *cobra.Command, args []string) {
		features.ShowTermuxTools()
		platform.ShowTermuxToolsStatus()
		platform.ShowTermuxAdvancedFeatures()
		platform.ShowTermuxBatteryOptimization()
	},
}