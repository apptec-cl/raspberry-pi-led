ENV['BUNDLE_GEMFILE'] ||= File.expand_path('../Gemfile', __dir__)

require 'bundler/setup' # Set up gems listed in the Gemfile.
# require 'bootsnap/setup' # Speed up boot time by caching expensive operations.
unless File.exists?("/proc/cpuinfo") && File.read("/proc/cpuinfo").include?("ARMv7")
  require 'bootsnap/setup'
end