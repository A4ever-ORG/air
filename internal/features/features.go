package features

import (
	"fmt"
	"runtime"
	"time"

	"github.com/awesome-project/go-multi-platform/internal/platform"
	"github.com/briandowns/spinner"
	"github.com/fatih/color"
	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
)

func ShowSystemInfo() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)
	blue := color.New(color.FgBlue, color.Bold)

	cyan.Println("🔍 System Information")
	fmt.Println()

	// Platform info
	info := platform.GetPlatformInfo()
	green.Printf("📍 Platform: %s\n", info.Name)
	yellow.Printf("🖥️  OS: %s %s\n", info.OS, info.Arch)
	blue.Printf("🐧 Kernel: %s\n", info.Kernel)
	fmt.Println()

	// CPU Info
	cpuInfo, err := cpu.Info()
	if err != nil {
		red.Printf("⚠️  CPU Info: Error retrieving CPU information (%v)\n", err)
	} else if len(cpuInfo) > 0 {
		green.Printf("⚡ CPU: %s\n", cpuInfo[0].ModelName)
		yellow.Printf("🔢 Cores: %d\n", runtime.NumCPU())
		
		cpuPercent, err := cpu.Percent(0, false)
		if err != nil {
			red.Printf("⚠️  CPU Usage: Error retrieving CPU usage (%v)\n", err)
		} else if len(cpuPercent) > 0 {
			red.Printf("📊 CPU Usage: %.1f%%\n", cpuPercent[0])
		}
	} else {
		red.Printf("⚠️  CPU Info: No CPU information available\n")
	}
	fmt.Println()

	// Memory Info
	memInfo, err := mem.VirtualMemory()
	if err != nil {
		red.Printf("⚠️  Memory Info: Error retrieving memory information (%v)\n", err)
	} else {
		green.Printf("💾 Total Memory: %.2f GB\n", float64(memInfo.Total)/1024/1024/1024)
		yellow.Printf("📈 Used Memory: %.2f GB (%.1f%%)\n", 
			float64(memInfo.Used)/1024/1024/1024, memInfo.UsedPercent)
		blue.Printf("📉 Available Memory: %.2f GB\n", float64(memInfo.Available)/1024/1024/1024)
	}
	fmt.Println()

	// Disk Info
	diskInfo, err := disk.Usage("/")
	if err != nil {
		red.Printf("⚠️  Disk Info: Error retrieving disk information (%v)\n", err)
	} else {
		green.Printf("💿 Total Disk: %.2f GB\n", float64(diskInfo.Total)/1024/1024/1024)
		yellow.Printf("📁 Used Disk: %.2f GB (%.1f%%)\n", 
			float64(diskInfo.Used)/1024/1024/1024, diskInfo.UsedPercent)
		blue.Printf("📂 Free Disk: %.2f GB\n", float64(diskInfo.Free)/1024/1024/1024)
	}
	fmt.Println()

	// Network Info
	netInfo, err := net.Interfaces()
	if err != nil {
		red.Printf("⚠️  Network Info: Error retrieving network information (%v)\n", err)
	} else {
		green.Println("🌐 Network Interfaces:")
		for _, iface := range netInfo {
			if len(iface.Addrs) > 0 {
				yellow.Printf("  📡 %s: %s\n", iface.Name, iface.Addrs[0].Addr)
			}
		}
	}
	fmt.Println()

	// Platform-specific features
	cyan.Println("🎯 Platform Features:")
	for i, feature := range info.Features {
		green.Printf("  %d. %s\n", i+1, feature)
	}
	fmt.Println()
}

func ShowNetworkTools() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("🌐 Network Analysis Tools")
	fmt.Println()

	info := platform.GetPlatformInfo()
	
	if info.IsKali {
		green.Println("⚔️ Kali Linux Network Tools:")
		yellow.Println("  • Nmap - Network scanning and discovery")
		yellow.Println("  • Wireshark - Packet analysis")
		yellow.Println("  • Aircrack-ng - Wireless network security")
		yellow.Println("  • Metasploit - Exploitation framework")
		yellow.Println("  • Burp Suite - Web application security")
	} else if info.IsTermux {
		green.Println("📱 Termux Network Tools:")
		yellow.Println("  • Nmap - Mobile network scanning")
		yellow.Println("  • Termux API - Android integration")
		yellow.Println("  • SSH client - Remote access")
		yellow.Println("  • Network utilities - ping, traceroute")
		yellow.Println("  • Mobile-optimized scanning")
	} else {
		green.Println("🖥️ Standard Network Tools:")
		yellow.Println("  • Basic network scanning")
		yellow.Println("  • Port detection")
		yellow.Println("  • Connection testing")
		yellow.Println("  • Network monitoring")
	}

	fmt.Println()
	red.Println("🚀 Advanced Features:")
	yellow.Println("  • Real-time network monitoring")
	yellow.Println("  • Automated vulnerability scanning")
	yellow.Println("  • Network traffic analysis")
	yellow.Println("  • Custom scanning profiles")
	yellow.Println("  • Export capabilities")
	fmt.Println()
}

func ShowSecurityTools() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("🔒 Security Analysis Tools")
	fmt.Println()

	info := platform.GetPlatformInfo()
	
	if info.IsKali {
		green.Println("⚔️ Kali Linux Security Suite:")
		yellow.Println("  • Penetration testing tools")
		yellow.Println("  • Vulnerability assessment")
		yellow.Println("  • Social engineering toolkit")
		yellow.Println("  • Password cracking tools")
		yellow.Println("  • Forensic analysis tools")
	} else if info.IsTermux {
		green.Println("📱 Termux Security Tools:")
		yellow.Println("  • Mobile security testing")
		yellow.Println("  • Android app analysis")
		yellow.Println("  • Network security scanning")
		yellow.Println("  • Basic penetration testing")
		yellow.Println("  • Security education tools")
	} else {
		green.Println("🖥️ Standard Security Tools:")
		yellow.Println("  • Basic security scanning")
		yellow.Println("  • System hardening")
		yellow.Println("  • Security monitoring")
		yellow.Println("  • Access control")
	}

	fmt.Println()
	red.Println("🛡️ Security Features:")
	yellow.Println("  • Automated security audits")
	yellow.Println("  • Real-time threat detection")
	yellow.Println("  • Security report generation")
	yellow.Println("  • Compliance checking")
	yellow.Println("  • Incident response tools")
	fmt.Println()
}

func ShowKaliTools() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("⚔️ Kali Linux Exclusive Tools")
	fmt.Println()

	green.Println("🎯 Penetration Testing:")
	yellow.Println("  • Metasploit Framework")
	yellow.Println("  • Nmap - Network discovery")
	yellow.Println("  • Wireshark - Packet analysis")
	yellow.Println("  • Aircrack-ng - Wireless security")
	yellow.Println("  • John the Ripper - Password cracking")
	fmt.Println()

	green.Println("🔍 Information Gathering:")
	yellow.Println("  • Maltego - OSINT framework")
	yellow.Println("  • Recon-ng - Reconnaissance")
	yellow.Println("  • TheHarvester - Email harvesting")
	yellow.Println("  • Sublist3r - Subdomain enumeration")
	yellow.Println("  • Shodan CLI - Internet scanning")
	fmt.Println()

	green.Println("💻 Exploitation Tools:")
	yellow.Println("  • BeEF - Browser exploitation")
	yellow.Println("  • Social Engineering Toolkit")
	yellow.Println("  • SQLmap - SQL injection")
	yellow.Println("  • Burp Suite - Web security")
	yellow.Println("  • OWASP ZAP - Web app testing")
	fmt.Println()

	red.Println("🚀 Advanced Features:")
	yellow.Println("  • Automated penetration testing")
	yellow.Println("  • Custom exploit development")
	yellow.Println("  • Advanced evasion techniques")
	yellow.Println("  • Post-exploitation tools")
	yellow.Println("  • Professional reporting")
	fmt.Println()
}

func ShowTermuxTools() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("📱 Termux Exclusive Features")
	fmt.Println()

	green.Println("📱 Mobile Optimization:")
	yellow.Println("  • Touch-friendly interface")
	yellow.Println("  • Battery optimization")
	yellow.Println("  • Mobile-optimized scanning")
	yellow.Println("  • Android API integration")
	yellow.Println("  • Gesture support")
	fmt.Println()

	green.Println("🔧 Android Integration:")
	yellow.Println("  • Termux API access")
	yellow.Println("  • Android sensor data")
	yellow.Println("  • Camera integration")
	yellow.Println("  • GPS location services")
	yellow.Println("  • Bluetooth scanning")
	fmt.Println()

	green.Println("📊 Mobile Security:")
	yellow.Println("  • Android app analysis")
	yellow.Println("  • Mobile network scanning")
	yellow.Println("  • WiFi security testing")
	yellow.Println("  • Bluetooth security")
	yellow.Println("  • Mobile forensics")
	fmt.Println()

	red.Println("🚀 Advanced Mobile Features:")
	yellow.Println("  • Offline capability")
	yellow.Println("  • Low-resource optimization")
	yellow.Println("  • Mobile-specific exploits")
	yellow.Println("  • Touch gesture controls")
	yellow.Println("  • Mobile reporting")
	fmt.Println()
}

func RunDemo() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)

	cyan.Println("🎮 Interactive Demo Mode")
	fmt.Println()

	// Create spinner
	s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
	s.Suffix = " Initializing demo..."
	s.Start()

	time.Sleep(2 * time.Second)
	s.Stop()

	green.Println("✅ Demo initialized successfully!")
	fmt.Println()

	// Platform-specific demo
	info := platform.GetPlatformInfo()
	
	if info.IsKali {
		runKaliDemo()
	} else if info.IsTermux {
		runTermuxDemo()
	} else {
		runGenericDemo()
	}
}

func runKaliDemo() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("⚔️ Kali Linux Demo")
	fmt.Println()

	demos := []struct {
		name        string
		description string
		duration    time.Duration
	}{
		{"Network Scanning", "Performing network discovery...", 3 * time.Second},
		{"Vulnerability Assessment", "Analyzing system vulnerabilities...", 4 * time.Second},
		{"Penetration Testing", "Running penetration tests...", 5 * time.Second},
		{"Forensic Analysis", "Collecting forensic data...", 3 * time.Second},
		{"Report Generation", "Generating security report...", 2 * time.Second},
	}

	for i, demo := range demos {
		green.Printf("🎯 Step %d: %s\n", i+1, demo.name)
		yellow.Printf("   %s\n", demo.description)
		
		s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
		s.Suffix = " Processing..."
		s.Start()
		
		time.Sleep(demo.duration)
		s.Stop()
		
		red.Printf("   ✅ Completed!\n\n")
	}

	green.Println("🎉 Kali Linux demo completed successfully!")
	fmt.Println()
}

func runTermuxDemo() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("📱 Termux Demo")
	fmt.Println()

	demos := []struct {
		name        string
		description string
		duration    time.Duration
	}{
		{"Mobile Optimization", "Optimizing for mobile...", 2 * time.Second},
		{"Android Integration", "Integrating with Android...", 3 * time.Second},
		{"Touch Interface", "Configuring touch controls...", 2 * time.Second},
		{"Battery Optimization", "Optimizing battery usage...", 2 * time.Second},
		{"Mobile Security", "Testing mobile security...", 4 * time.Second},
	}

	for i, demo := range demos {
		green.Printf("📱 Step %d: %s\n", i+1, demo.name)
		yellow.Printf("   %s\n", demo.description)
		
		s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
		s.Suffix = " Processing..."
		s.Start()
		
		time.Sleep(demo.duration)
		s.Stop()
		
		red.Printf("   ✅ Completed!\n\n")
	}

	green.Println("🎉 Termux demo completed successfully!")
	fmt.Println()
}

func runGenericDemo() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("🖥️ Generic Linux Demo")
	fmt.Println()

	demos := []struct {
		name        string
		description string
		duration    time.Duration
	}{
		{"System Analysis", "Analyzing system...", 3 * time.Second},
		{"Network Testing", "Testing network connectivity...", 2 * time.Second},
		{"Security Check", "Performing security checks...", 3 * time.Second},
		{"Performance Test", "Testing performance...", 2 * time.Second},
	}

	for i, demo := range demos {
		green.Printf("🖥️ Step %d: %s\n", i+1, demo.name)
		yellow.Printf("   %s\n", demo.description)
		
		s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
		s.Suffix = " Processing..."
		s.Start()
		
		time.Sleep(demo.duration)
		s.Stop()
		
		red.Printf("   ✅ Completed!\n\n")
	}

	green.Println("🎉 Generic demo completed successfully!")
	fmt.Println()
}